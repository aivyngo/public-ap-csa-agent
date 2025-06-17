from agents import Agent, Runner
from tools.utils import make_tool

async def generate_question(topic: str, qtype: str) -> str:
    agent = Agent(
        name="Question Generator",
        instructions=f"""
        You are a CollegeBoard AP Computer Science A (AP CSA) question generator.
        Given the following inputs:
        - Topic: {topic}
        - Question type: {qtype} (either "multiple choice" or "free response")
        Generate a clear, well-formed AP-style question on the topic.
        If it is multiple choice, include the choices and the correct answer clearly.
        If it is free response, generate a detailed question suitable for open-ended coding or conceptual response.
        Return only the question and choices (if any) in your output.
        """
        ,
        model="gpt-4o"
    )
    prompt = f"Topic: {topic}\nQuestion type: {qtype}"
    return await Runner.run(agent, prompt)

generate_question = make_tool(
    generate_question,
    name="generate_question",
    description="Generates an AP CSA-style question for a given topic and type.",
    param_schema={
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "The AP CSA topic (e.g., arrays, inheritance)"},
            "qtype": {"type": "string", "description": "Question type: 'multiple choice' or 'free response'"}
        },
        "required": ["topic", "qtype"]
    }
)