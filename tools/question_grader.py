import re
from agents import Agent, Runner
from tools.utils import make_tool

async def grade_question(question: str, response: str, rubric: str = None) -> tuple[str, str]:
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
        model="gpt-4o"
    )

    prompt = f"""
    Question: {question}
    Student's Response: {response}
    Rubric: {rubric if rubric else "No rubric provided. Please generate one."}
    """

    raw_output = await Runner.run(agent, prompt)

    # Try to extract score using regex
    score_match = re.search(r"Score:\s*(\d+\/\d+)", raw_output)
    if score_match:
        score = score_match.group(1)
    else:
        score = "Score not found"

    # Try to extract feedback section (everything after "Feedback:")
    feedback_match = re.search(r"Feedback:\s*(.*)", raw_output, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else raw_output.strip()

    return score, feedback

grade_question = make_tool(
    grade_question,
    name="grade_question",
    description="Grades a student's response to an AP CSA question using a rubric.",
    param_schema={
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The AP CSA question being answered"},
            "response": {"type": "string", "description": "The student's answer"},
            "rubric": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of rubric points required for full credit"
            }
        },
        "required": ["question", "response", "rubric"]
    }
)