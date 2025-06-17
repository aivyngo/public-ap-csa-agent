from fastapi import FastAPI
from models.models import PromptRequest, PromptResponse
from tools.apcsa_agent import run_apcsa_agent
from models.models import QuestionGeneratorRequest, QuestionGeneratorResponse
from tools.question_generator import generate_question
from tools.question_grader import grade_question
from models.models import QuestionGraderResponse, QuestionGraderRequest
from models.models import WebSearchResponse, WebSearchRequest
from tools.web_search import web_search
from models.models import TextbookResponse, TextbookRequest
from tools.textbook_search import textbook_search
from fastapi import FastAPI, HTTPException
from models.models import ToolCallRequest, ToolCallResponse
from tools.registry import TOOL_REGISTRY

app = FastAPI()

# just testing the agent in basic
@app.post("/apcsa-agent", response_model=PromptResponse)
async def apcsa_agent_endpoint(request: PromptRequest):
    response = await run_apcsa_agent(request.prompt)
    return PromptResponse(response=response)

# testing the basic question generator tool for now
@app.post("/question-generator", response_model=QuestionGeneratorResponse)
async def question_generator_endpoint(request: QuestionGeneratorRequest):
    question = await generate_question(request.topic, request.qtype)
    return QuestionGeneratorResponse(question=question)

# testing question grader
@app.post("/grade", response_model=QuestionGraderResponse)
async def grade(req: QuestionGraderRequest):
    score, feedback = await grade_question(req.question, req.response, req.rubric)
    return QuestionGraderResponse(score=score, feedback=feedback)

@app.post("/web_search", response_model=WebSearchResponse)
async def web_search_endpoint(request: WebSearchRequest):
    relevant_info = await web_search(request.topic)
    return WebSearchResponse(relevant_info=relevant_info)

@app.post("/textbook_search", response_model=TextbookResponse)
async def textbook_search_endpoint(request: TextbookRequest):
    relevant_info = await textbook_search(request.topic)
    return TextbookResponse(relevant_info=relevant_info)

@app.post("/call_tool", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    tool_fn = TOOL_REGISTRY.get(request.tool_name)
    if not tool_fn:
        raise HTTPException(status_code=400, detail=f"Tool '{request.tool_name}' not found.")

    try:
        result = await tool_fn(**request.parameters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling tool: {str(e)}")

    return ToolCallResponse(request_id=request.request_id, result=result)

@app.get("/")
async def root():
    return {"message": "API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
