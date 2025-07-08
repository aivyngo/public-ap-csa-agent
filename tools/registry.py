from tools.question_generator import generate_question_tool
from tools.question_grader import grade_question_tool
from tools.web_search import web_search_tool
from tools.textbook_search import textbook_search_tool

TOOL_REGISTRY = {
    "generate_question": generate_question_tool,
    "grade_question": grade_question_tool,
    "web_search": web_search_tool,
    "textbook_search": textbook_search_tool,
}