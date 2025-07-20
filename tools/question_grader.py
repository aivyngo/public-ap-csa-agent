import re
from datetime import datetime
from agents import Agent, Runner
from models.models import QuestionGraderInput, QuestionGraderOutput

async def grade_question(input: QuestionGraderInput, request_id: str) -> QuestionGraderOutput:
    agent = Agent(
        name="Question Grader",
        instructions="""
        You are an AP Computer Science A grader.
        Given:
        - A question
        - A student’s response
        - (Optionally) a rubric
        Do the following:
        1. If no rubric is provided, generate one that reflects typical AP/College Board grading style.
        2. Use the rubric to grade the student's response.
        3. Give point-by-point feedback and part-by part feedback if the question has multiple parts:
           - State how many points were earned for each rubric item
           - Explain the correct answer and what the student got right/wrong
        4. Provide a final score (ex. 5/7).
        5. Be fair, clear, and concise.
        Format your response exactly like this:

        Score: [score]

        Feedback:
        [detailed feedback here]
        """,
        model= "gpt-4o"
    )

    prompt_messages = [
        {
            "role": "user",
            "content": f"""
Question: {input.question}
Student's Response: {input.response}
Rubric: {input.rubric if input.rubric else "No rubric provided. Please generate one."}
            """.strip()
        }
    ]

    raw_output = await Runner.run(agent, prompt_messages)

    # Extract score
    score_match = re.search(r"Score:\s*(\d+\/\d+)", raw_output)
    score = score_match.group(1) if score_match else "Score not found"

    # Extract feedback
    feedback_match = re.search(r"Feedback:\s*(.*)", raw_output, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else raw_output.strip()

    return QuestionGraderOutput(
        tool_name="grade_question",
        request_id=request_id,
        status="success",
        score=score,
        feedback=feedback,
        timestamp=datetime.utcnow().isoformat()
    )
