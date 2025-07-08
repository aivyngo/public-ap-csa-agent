from pydantic import BaseModel
from typing import Optional, List, Literal, Union

# Define the schema using Pydantic
# QUESTION GENERATOR TOOL
class QuestionGeneratorInput(BaseModel): # input schema
    topic: str
    qtype: str # mcq or frq

class QuestionGeneratorOutput(BaseModel): # output schema
    tool_name: Literal["generate_question"]
    request_id: str
    status: str
    question: str
    timestamp: str

# QUESTION GRADER TOOL
class QuestionGraderInput(BaseModel): # input schema
    question: str
    response: str
    rubric: Optional[str] = None

class QuestionGraderOutput(BaseModel): # output schema
    tool_name: Literal["grade_question"]
    request_id: str
    status: str
    score: str
    feedback: str
    timestamp: str

# WEB SEARCH TOOL
class WebSearchInput(BaseModel): # input schema
    topic: str

class WebSearchOutput(BaseModel): # output schema
    tool_name: Literal["web_search"]
    request_id: str
    status: str
    relevant_info: str
    timestamp: str

# TEXTBOOK SEARCH TOOL
class TextbookSearchInput(BaseModel): # input schema
    topic: str

class TextbookSearchOutput(BaseModel): # output schema
    tool_name: Literal["textbook_search"]
    request_id: str
    status: str
    relevant_info: str
    timestamp: str

class ToolCallInput(BaseModel):
    tool_name: Literal[
        "generate_question",
        "grade_question",
        "web_search",
        "textbook_search"
    ]
    parameters: Union[
        QuestionGeneratorInput,
        QuestionGraderInput,
        WebSearchInput,
        TextbookSearchInput
    ]
    request_id: str

# ToolCallResponse
class ToolCallOutput(BaseModel):
    request_id: str
    result: Union[
        QuestionGeneratorOutput,
        QuestionGraderOutput,
        WebSearchOutput,
        TextbookSearchOutput
    ]

class ToolUse(BaseModel):
    tool_name: Literal['generate_question', 'grade_question', 'web_search', 'textbook_search']
    parameters: Union[QuestionGeneratorInput,
        QuestionGraderInput,
        WebSearchInput,
        TextbookSearchInput]
    tool_result: Union[QuestionGeneratorOutput,
        QuestionGraderOutput,
        WebSearchOutput,
        TextbookSearchOutput]

class TaskLV5(BaseModel):
    thought: str
    tooluse: Optional[ToolUse] = None
    conclusion: str
    title: str

class TaskLV4(BaseModel):
    thought: str
    # tooluse: Optional[Union[ToolUse, str]] = None
    tooluse: Optional[ToolUse] = None
    subtasks: Optional[List[TaskLV5]] = None
    conclusion: str
    title: str

class TaskLV3(BaseModel):
    thought: str
    # tooluse: Optional[Union[ToolUse, str]] = None
    tooluse: Optional[ToolUse] = None
    subtasks: Optional[List[TaskLV4]] = None
    conclusion: str
    title: str

class TaskLV2(BaseModel):
    thought: str
    # tooluse: Optional[Union[ToolUse, str]] = None
    tooluse: Optional[ToolUse] = None
    subtasks: Optional[List[TaskLV3]] = None
    conclusion: str
    title: str

class Task(BaseModel):
    thought: str
    tooluse: Optional[ToolUse] = None
    subtasks: Optional[List[TaskLV2]] = None
    conclusion: str
    title: str

Task.model_rebuild()

class Solution(BaseModel):
    tasks: List[Task]