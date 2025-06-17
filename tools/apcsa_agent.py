from agents import Agent, Runner
from tools.question_grader import grade_question
from tools.question_generator import generate_question
from tools.web_search import web_search


async def run_apcsa_agent(prompt: str) -> str:
    agent = Agent(
        name="AP CSA Tutor",
        instructions="""
You are an AP Computer Science A (AP CSA) teaching assistant with access to these tools:
- web_search: Search the web for relevant AP CSA and Java information.
- generate_question: Generate AP CSA-style questions given a topic and question type.
- grade_question: Grade a student's answer given a rubric.

Given a topic, follow these steps carefully:
1. Use web_search to find relevant concepts, examples, or problems related to the topic.
2. Use generate_question to create a well-formed AP CSA-style question testing understanding of that topic.
3. Create a detailed rubric listing the key points or steps required for a correct answer.
4. Attempt to answer the problem yourself.
5. If the question cannot be answered due to insufficient or unclear information, generate a better, answerable problem on the same topic.
6. Check whether each point in the rubric is valid and necessary—remove any unnecessary criteria.
7. If the question is answerable and the rubric is valid, return the following:
- The final problem
- The final rubric
- Your answer

Use the tools by invoking their function calls where appropriate.
""",
        tools=[grade_question, generate_question, web_search],
        model="gpt-4o"
    )
    return await Runner.run(agent, prompt)
