from agents import Agent, Runner
import json
import requests
from openai import OpenAI
from tools.question_grader import grade_question
from tools.question_generator import generate_question
from tools.web_search import web_search
from tools.textbook_search import textbook_search
from typing import List, Optional, Union, Literal, Any, Dict

# async def run_apcsa_agent(prompt: str) -> str:
#async def run_apcsa_agent(msg_list: List) -> str:
    #agent = Agent(
        #name="AP CSA Tutor",
        #instructions="""
#You are an AP Computer Science A (AP CSA) teaching assistant with access to these tools:
#- web_search_tool: Search the web for relevant AP CSA and Java information.
#- generate_question_tool: Generate AP CSA-style questions given a topic and question type. The question should fit'
#    'into one of four types: '
#    'Question 1: Methods and Control Structures—Students will be asked to write program code to create objects of a class and call methods, and satisfy method specifications using expressions, conditional statements, and iterative statements.'
#    'Question 2: Classes—Students will be asked to write program code to define a new type by creating a class and satisfy method specifications using expressions, conditional statements, and iterative statements. '
#    'Question 3: Array/ArrayList—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 1D array or ArrayList objects. '
#    'Question 4: 2D Array—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 2D array objects.'
#    'Ensure that all generated questions are in the scope of the class by comparing them to questions you find on the web. For example, hashsets and hashmaps are NOT in the scope of the class. Topics covered include'
#    'primitieve types, using objects, boolean expressions, iteration, writing classes, arrays, arraylists, 2d arrays, inheritance, and recursion.'
#- grade_question_tool: Grade a student's answer given a rubric. If not given a rubric, generate your own.
#- textbook_search_tool: Search the textbook for relevant information.

#Use the tools by invoking their function calls where appropriate.
#""",
#        tools=[grade_question_tool, generate_question_tool, web_search_tool, textbook_search_tool],
#        model="gpt-4o"
#    )
#    response = await Runner.run(agent, msg_list)
#    if isinstance(response, dict) or isinstance(response, list):
#        return json.dumps(response, indent=2)  # as fallback
#    return str(response)

openai_client = OpenAI(
    base_url = "http://192.222.54.121:8081/v1",
    api_key = "test-key"
)

async def run_apcsa_agent(msg_list: List) -> str:
    resp = openai_client.chat.completions.create(
        model="tim-large",  
        messages=msg_list,
        temperature=0.6,
        max_completion_tokens=4096,
        tools=[
            {
                "type": "function",
                "name": "generate_question",
                "description": "Generate AP CSA-style questions given a topic and question type. The question should fit into one of four types:"
                                'Question 1: Methods and Control Structures—Students will be asked to write program code to create objects of a class and call methods, and satisfy method specifications using expressions, conditional statements, and iterative statements.'
                                'Question 2: Classes—Students will be asked to write program code to define a new type by creating a class and satisfy method specifications using expressions, conditional statements, and iterative statements. '
                                'Question 3: Array/ArrayList—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 1D array or ArrayList objects. '
                                'Question 4: 2D Array—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 2D array objects.'
                                'Ensure that all generated questions are in the scope of the class by comparing them to questions you find on the web. For example, hashsets and hashmaps are NOT in the scope of the class. Topics covered include'
                                "primitieve types, using objects, boolean expressions, iteration, writing classes, arrays, arraylists, 2d arrays, inheritance, and recursion.",
                "url": "http://192.222.54.121:8060/call_tool",
                "method": "POST",
                "timeout": 10,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to generate a question on."
                        },
                        "qtype": {
                            "type": "string",
                            "description": "Type of question: multiple_choice or free_response."
                        }
                    },
                    "required": ["topic", "qtype"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",  
                "name": "grade_question",
                "description": "Grade a student's answer given a rubric. If not given a rubric, generate your own.",
                "url": "http://192.222.54.121:8060/call_tool",
                "method": "POST",
                "timeout": 10,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string",
                                     "description": "Question that is being answered."},
                        "response": {"type": "string",
                                     "description": "response to the question"},
                        "rubric": {"type": "array", "items": {"type": "string"},
                                   "description": "rubric used to grade the question."}
                    },
                    "required": ["question", "response", "rubric"],
                    "additionalProperties": False
                }
                
            },
            {
                "type": "function",
                "name": "web_search",
                "description": "Search the web for relevant AP CSA and Java information.",
                "url": "http://192.222.54.121:8060/call_tool",
                "method": "POST",
                "timeout": 10,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string",
                                  "description": "topic to search for on the web related to AP CSA."}
                    },
                    "required": ["topic"],
                    "additionalProperties": False
                }
    
            },
            {
                "type": "function",  
                "name": "textbook_search",
                "description": "Search the textbook for relevant information.",
                "url": "http://192.222.54.121:8060/call_tool",
                "method": "POST",
                "timeout": 10,
                "parameters": {
                   "type": "object",
                    "properties": {
                        "topic": {"type": "string",
                                  "description": "topic to search for in the textbook."}
                    },
                    "required": ["topic"],
                    "additionalProperties": False
                }
            }
        ]
    )   
    
    #return resp.choices[0].message.content
    return (json.loads(resp.choices[0].message.content)['answer'])