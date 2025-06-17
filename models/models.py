from pydantic import BaseModel
from typing import Optional
from typing import Dict, Any

# testing basic agent
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

class QuestionGeneratorRequest(BaseModel):
    topic: str # topic question
    qtype: str  # mcq vs frq

class QuestionGeneratorResponse(BaseModel):
    question: str  # generated question

class QuestionGraderRequest(BaseModel):
    question: str # question answered
    response: str # student answer
    rubric: Optional[str] = None

class QuestionGraderResponse(BaseModel):
    score: str # ex. 5/7
    feedback: str # feedback in words

class WebSearchRequest(BaseModel):
    topic: str

class WebSearchResponse(BaseModel):
    relevant_info: str

class TextbookRequest(BaseModel):
    topic: str

class TextbookResponse(BaseModel):
    relevant_info: str

class ToolCallRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    request_id: str

class ToolCallResponse(BaseModel):
    request_id: str
    result: Any