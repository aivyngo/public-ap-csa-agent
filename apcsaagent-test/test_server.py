import json
import requests

from sglang.utils import print_highlight
from think_models import *

port = 30000

# System prompt setup
sys_msg_list = [
    '<|im_start|>system\nYou are Tim. You are a helpful assistant. You are encouraged to use the following tools:\n',
    '- generate_question: generate AP CSA questions based on a topic and question type. The question should fit'
    'into one of four types: '
    'Question 1: Methods and Control Structures—Students will be asked to write program code to create objects of a class and call methods, and satisfy method specifications using expressions, conditional statements, and iterative statements.'
    'Question 2: Classes—Students will be asked to write program code to define a new type by creating a class and satisfy method specifications using expressions, conditional statements, and iterative statements. '
    'Question 3: Array/ArrayList—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 1D array or ArrayList objects. '
    'Question 4: 2D Array—Students will be asked to write program code to satisfy method specifications using expressions, conditional statements, and iterative statements and create, traverse, and manipulate elements in 2D array objects.'
    'Ensure that all generated questions are in the scope of the class by comparing them to questions you find on the web. For example, hashsets and hashmaps are NOT in the scope of the class. Topics covered include'
    'primitieve types, using objects, boolean expressions, iteration, writing classes, arrays, arraylists, 2d arrays, inheritance, and recursion.',
    '- grade_question: grade student responses to AP CSA questions.',
    '- web_search: search the web for relevant AP CSA info.',
    '- textbook_search: search the AP CSA textbook PDF for relevant info.',
    'Do not generate any indent.<|im_end|>'
]
system_prompt = '\n'.join(sys_msg_list)

# User question
research_question = "Generate a free response question on ArrayLists."
research_prompts = [
    f"""{system_prompt}\n<|im_start|>user\n{research_question}<|im_end|>\n<|im_start|>assistant\n"""
]

# Call /generate
response = requests.post(
    f"http://192.222.54.121:{port}/generate",
    json={
        "text": research_prompts[0],
        "sampling_params": {
            "top_p": 0.95,
            "max_new_tokens": 40000,
            "temperature": 0.6,
            "json_schema": json.dumps(Task.model_json_schema()),
            "tool_list": [
                {
                    "name": "generate_question",
                    "url": "http://192.222.54.121:8060/call_tool",
                    "method": "POST",
                    "timeout": 10
                },
                {
                    "name": "grade_question",
                    "url": "http://192.222.54.121:8060/call_tool",
                    "method": "POST",
                    "timeout": 10
                },
                {
                    "name": "web_search",
                    "url": "http://192.222.54.121:8060/call_tool",
                    "method": "POST",
                    "timeout": 10
                },
                {
                    "name": "textbook_search",
                    "url": "http://192.222.54.121:8060/call_tool",
                    "method": "POST",
                    "timeout": 10
                }
            ]
        }
    }
)

# Parse the response
response_json = response.json()
if "text" not in response_json:
    print("❌ 'text' not found in response.")
    print("Full response:", response_json)
    exit(1)

res_str = response_json["text"]  # This is a stringified JSON result
res_obj = json.loads(res_str)    # Convert string to Python dict

# Save as JSON
json.dump(res_obj, open('ans.json', 'w'))

# Convert JSON to Markdown
cur_params = {
    "tool_name": 'JsonToMarkdown',
    "parameters": {
        'json_string': res_str  # keep as string
    },
}

# Send to conversion tool
url = "http://192.222.54.121:8060/call_tool"
response = requests.post(url, json=cur_params)

res = response.json()
markdown = res.get('markdown', '')

# Save Markdown
open('ans.md', 'w').write(markdown)
