from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm_adapter import suggest_learning_path

router = APIRouter()

class LearningPathRequest(BaseModel):
    topic: str
    level: str  # beginner, intermediate, advanced

class LearningPathResponse(BaseModel):
    path: list[str]

@router.post("/", response_model=LearningPathResponse)
async def learning_path(request: LearningPathRequest):
    path = suggest_learning_path(request.topic, request.level)
    return LearningPathResponse(path=path)
