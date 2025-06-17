from tools.question_generator import generate_question
from tools.question_grader import grade_question
from tools.web_search import web_search
from tools.textbook_search import textbook_search

TOOL_REGISTRY = {
    "QuestionGenerator": generate_question,
    "QuestionGrader": grade_question,
    "WebSearch": web_search,
    "TextbookSearch": textbook_search,
}