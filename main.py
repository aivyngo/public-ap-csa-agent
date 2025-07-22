from fastapi import FastAPI, HTTPException
from fastapi import Request
from datetime import datetime
import json, re
from models.models import (
    QuestionGeneratorInput, QuestionGeneratorOutput,
    QuestionGraderInput, QuestionGraderOutput,
    WebSearchInput, WebSearchOutput,
    TextbookSearchInput, TextbookSearchOutput,
    ToolCallInput, ToolCallOutput
)
#from tools.apcsa_agent import run_apcsa_agent
from tools.question_generator import generate_question
from tools.question_grader import grade_question
from tools.web_search import web_search
from tools.textbook_search import textbook_search
from tools.apcsa_agent import run_apcsa_agent
from tools.registry import TOOL_REGISTRY
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# testing the basic question generator tool for now
@app.post("/question-generator", response_model=QuestionGeneratorOutput)
async def question_generator_endpoint(request: QuestionGeneratorInput):
    request_id = datetime.utcnow().isoformat()
    question_output = await generate_question(request, request_id)
    return question_output

# testing question grader
@app.post("/grade", response_model=QuestionGraderOutput)
async def grade_endpoint(req: QuestionGraderInput):
    request_id = datetime.utcnow().isoformat()
    output = await grade_question(req, request_id)
    return output

@app.post("/web_search", response_model=WebSearchOutput)
async def web_search_endpoint(request: WebSearchInput):
    request_id = datetime.utcnow().isoformat()
    output = await web_search(request, request_id)
    return output

@app.post("/textbook_search", response_model=TextbookSearchOutput)
async def textbook_search_endpoint(request: TextbookSearchInput):
    request_id = datetime.utcnow().isoformat()
    output = await textbook_search(request, request_id)
    return output

@app.post("/call_tool", response_model=ToolCallOutput)
async def call_tool(request: ToolCallInput):
    print("📞 Received tool call:", request.tool_name, request.request_id)
    tool_fn = TOOL_REGISTRY.get(request.tool_name)
    if not tool_fn:
        raise HTTPException(status_code=400, detail=f"Tool '{request.tool_name}' not found.")

    try:
        result = await tool_fn(request.parameters, request_id=request.request_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling tool: {str(e)}")
    
    print(f"Returning result type: {type(result)}")
    print(f"Result dict: {result.dict() if hasattr(result, 'dict') else result}")

    # return result
    return ToolCallOutput(request_id=request.request_id, result=result)

@app.get("/")
async def root():
    return {"message": "API is running!"}

# for openwebui
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    stream = body.get("stream", False)

    if not messages:
        return JSONResponse({"error": "No messages provided."}, status_code=400)

    # user_message = messages[-1].get("content", "")
    input_msgs = [
        {'role': 'system', 'content': 'You are given an instruction about AP CS test. Respond to it without overthinking. Use each tool at most Once.'}
    ] + messages
    agent_response = await run_apcsa_agent(input_msgs)
    print("🔍 Agent Response:\n", agent_response)

    # Convert dict/list to string if needed
    if isinstance(agent_response, (dict, list)):
        agent_response = json.dumps(agent_response, indent=2)

    if not agent_response.strip():
        agent_response = "[No response generated]"

    full_data = {
        "id": "chatcmpl-custom-agent",
        "object": "chat.completion",
        "created": int(datetime.utcnow().timestamp()),
        "model": "tim-large",
        "choices": [
            {
                "index": 0,
                "delta" if stream else "message": {
                    "role": "assistant",
                    "content": agent_response if not stream else ""
                },
                "finish_reason": None if stream else "stop"
            }
        ],
    }

    if not stream:
        # Normal non-streaming response
        full_data["usage"] = {
            "prompt_tokens": 0,
            "completion_tokens": len(agent_response.split()),
            "total_tokens": len(agent_response.split())
        }
        return JSONResponse(full_data)

    # Streaming mode — simulate chunks
    async def event_generator():
        yield f"data: {json.dumps({'choices': [{'delta': {'role': 'assistant'}}]})}\n\n"
        # Simulate word-by-word or chunked stream
        for chunk in agent_response.split(" "):
            await asyncio.sleep(0.05)
            yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk + ' '}}]})}\n\n"
        # Finish
        yield f"data: {json.dumps({'choices': [{'finish_reason': 'stop'}]})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "tim-large",
                "object": "model",
                "created": int(datetime.utcnow().timestamp()),
                "owned_by": "apcsa-agent"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8060, reload=True)