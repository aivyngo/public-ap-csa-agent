from datetime import datetime
from agents import Agent, Runner
from models.models import QuestionGeneratorInput, QuestionGeneratorOutput

async def generate_question(input: QuestionGeneratorInput, request_id: str) -> QuestionGeneratorOutput:
    agent = Agent(
        name="Question Generator",
        instructions=f"""
        You are a CollegeBoard AP Computer Science A (AP CSA) question generator.
        Given the following inputs:
        - Topic: {input.topic}
        - Question type: {input.qtype} (either "multiple choice" or "free response")
        Generate a clear, well-formed AP-style question on the topic. The question should fit
        into one of four types:
        Question 1: Methods and Control Structures—Students will be asked to write program code to create objects of a class and call methods, and satisfy method specifications using expressions, conditional statements, and iterative statements.
        Question 2: Classes—Students will be asked to write program code to define a new type by creating a class and satisfy method specifications using expressions, conditional statements, and iterative statements.
        Question 3: Array/ArrayList—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 1D array or ArrayList objects.
        Question 4: 2D Array—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 2D array objects.
        Ensure that all generated questions are in the scope of the class by comparing them to questions you find on the web. For example, hashsets and hashmaps are NOT in the scope of the class. Topics covered include primitive types, using objects, boolean expressions, iteration, writing classes, arrays, arraylists, 2d arrays, inheritance, and recursion.
        If it is multiple choice, include the choices and the correct answer clearly.
        If it is free response, generate a detailed question suitable for open-ended coding or conceptual response.
        Return only the question and choices (if any) in your output.
        """,
        model= "gpt-4o" #"tim-large"
    )

    # Wrap prompt in list of dicts with user role
    prompt_messages = [
        {"role": "user", "content": f"Topic: {input.topic}\nQuestion type: {input.qtype}"}
    ]

    generated_question = await Runner.run(agent, prompt_messages)

    return QuestionGeneratorOutput(
        tool_name="generate_question",
        request_id=request_id,
        status="success",
        question=generated_question,
        timestamp=datetime.utcnow().isoformat()
    )
