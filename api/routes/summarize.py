from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm_adapter import generate

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    summary: str

@router.post("/", response_model=TextResponse)
async def summarize_text(request: TextRequest):
    summary = generate(request.text)
    return TextResponse(summary=summary)
