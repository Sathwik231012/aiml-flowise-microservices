from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm_adapter import answer_question

router = APIRouter()

class QARequest(BaseModel):
    question: str
    context: str  # document text

class QAResponse(BaseModel):
    answer: str

@router.post("/", response_model=QAResponse)
async def qa(request: QARequest):
    answer = answer_question(request.question, request.context)
    return QAResponse(answer=answer)
