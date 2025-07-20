from tools.question_generator import generate_question
from tools.question_grader import grade_question
from tools.web_search import web_search
from tools.textbook_search import textbook_search

TOOL_REGISTRY = {
    "generate_question": generate_question,
    "grade_question": grade_question,
    "web_search": web_search,
    "textbook_search": textbook_search,
}