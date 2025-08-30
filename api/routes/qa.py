# api/routes/qa.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from ..services import rag
from ..services.llm_adapter import generate

router = APIRouter()

class QARequest(BaseModel):
    question: str
    top_k: int = 4

class QAResponse(BaseModel):
    answer: str
    sources: list

@router.post("/", response_model=QAResponse)
async def qa(request: QARequest = Body(...)):
    """
    RAG-powered QA: retrieve top_k chunks, build a context, and ask the LLM to answer using only those snippets.
    """
    results = rag.retrieve(request.question, top_k=request.top_k)
    if not results:
        return {"answer": "No documents indexed. Upload documents first via /docs/upload", "sources": []}

    context_snippets = []
    sources = []
    for text, meta, dist in results:
        file = meta.get("file", "unknown")
        chunk_id = meta.get("chunk_id", -1)
        context_snippets.append(f"[{file} | chunk:{chunk_id}] {text}")
        sources.append({"file": file, "chunk_id": chunk_id, "score": dist})

    context = "\n\n".join(context_snippets)

    prompt = (
        "You are a helpful assistant. Answer the question using ONLY the provided snippets. "
        "Cite sources inline using the [file|chunk] tag next to the sentence that uses the info. "
        "If the answer is not present in the snippets, respond: 'I don't know.' Keep the answer concise.\n\n"
        f"SNIPPETS:\n{context}\n\nQUESTION: {request.question}\n\nAnswer:"
    )

    answer = generate(prompt, temperature=0.0, max_tokens=400)
    return {"answer": answer, "sources": sources}
