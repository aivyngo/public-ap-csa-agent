import json
from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from typing import List, Callable, Optional

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class Agent:
    def __init__(self, name: str, instructions: str, model: str = "gpt-4o", tools: Optional[List[Callable]] = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []

class Runner:
    @staticmethod
    async def run(agent: Agent, user_prompt: str):
        functions = []
        for tool in agent.tools:
            if hasattr(tool, "name") and hasattr(tool, "description") and hasattr(tool, "parameters"):
                functions.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                })

        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": user_prompt}
        ]

        # Prepare request arguments
        request_kwargs = {
            "model": agent.model,
            "messages": messages,
            "temperature": 0.7,
        }

        # Only add functions & function_call if functions list is not empty
        if functions:
            request_kwargs["functions"] = functions
            request_kwargs["function_call"] = "auto"

        while True:
            response = await client.chat.completions.create(**request_kwargs)

            message = response.choices[0].message

            if message.function_call is not None:
                func_call = message.function_call
                func_name = func_call.name
                func_args = json.loads(func_call.arguments or "{}")

                tool_fn = next((t for t in agent.tools if t.name == func_name), None)
                if tool_fn is None:
                    raise ValueError(f"Tool '{func_name}' not found")

                tool_result = await tool_fn(**func_args)

                messages.append(message)  # model's function call message
                messages.append({
                    "role": "function",
                    "name": func_name,
                    "content": tool_result
                })

                request_kwargs["messages"] = messages
            else:
                return message.content
