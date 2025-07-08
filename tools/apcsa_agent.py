from agents import Agent, Runner
import json
from tools.question_grader import grade_question_tool
from tools.question_generator import generate_question_tool
from tools.web_search import web_search_tool
from tools.textbook_search import textbook_search_tool
from typing import List

# async def run_apcsa_agent(prompt: str) -> str:
async def run_apcsa_agent(msg_list: List) -> str:
    agent = Agent(
        name="AP CSA Tutor",
        instructions="""
You are an AP Computer Science A (AP CSA) teaching assistant with access to these tools:
- web_search_tool: Search the web for relevant AP CSA and Java information.
- generate_question_tool: Generate AP CSA-style questions given a topic and question type. The question should fit'
    'into one of four types: '
    'Question 1: Methods and Control Structures—Students will be asked to write program code to create objects of a class and call methods, and satisfy method specifications using expressions, conditional statements, and iterative statements.'
    'Question 2: Classes—Students will be asked to write program code to define a new type by creating a class and satisfy method specifications using expressions, conditional statements, and iterative statements. '
    'Question 3: Array/ArrayList—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 1D array or ArrayList objects. '
    'Question 4: 2D Array—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 2D array objects.'
    'Ensure that all generated questions are in the scope of the class by comparing them to questions you find on the web. For example, hashsets and hashmaps are NOT in the scope of the class. Topics covered include'
    'primitieve types, using objects, boolean expressions, iteration, writing classes, arrays, arraylists, 2d arrays, inheritance, and recursion.'
- grade_question_tool: Grade a student's answer given a rubric. If not given a rubric, generate your own.
- textbook_search_tool: Search the textbook for relevant information.

Use the tools by invoking their function calls where appropriate.
""",
        tools=[grade_question_tool, generate_question_tool, web_search_tool, textbook_search_tool],
        model="gpt-4o"
    )
    response = await Runner.run(agent, msg_list)
    if isinstance(response, dict) or isinstance(response, list):
        return json.dumps(response, indent=2)  # as fallback
    return str(response)
