# api/routes/docs_upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import fitz  # PyMuPDF
from ..services import rag
import io

router = APIRouter()

def extract_text_from_pdf_bytes(b: bytes) -> str:
    """
    Extract text from PDF bytes using PyMuPDF (fitz).
    """
    doc = fitz.open(stream=b, filetype="pdf")
    pages = []
    for p in doc:
        pages.append(p.get_text())
    return "\n".join(pages)

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """
    Sliding window chunker.
    """
    text = text.replace("\r\n", "\n")
    chunks = []
    i = 0
    L = len(text)
    while i < L:
        end = min(i + chunk_size, L)
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= L:
            break
        i = max(end - overlap, i + 1)
    return chunks

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT file and index its chunks into the vector DB.
    Returns: {"file": filename, "chunks_indexed": N}
    """
    filename = file.filename or "unnamed"
    lower = filename.lower()
    if not (lower.endswith(".pdf") or lower.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files supported")

    content = await file.read()
    if lower.endswith(".pdf"):
        try:
            text = extract_text_from_pdf_bytes(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {e}")
    else:
        try:
            text = content.decode("utf-8", errors="ignore")
        except Exception:
            text = str(content)

    chunks = chunk_text(text, chunk_size=1200, overlap=200)
    metadatas = [{"file": filename, "chunk_id": idx} for idx, _ in enumerate(chunks)]
    count = rag.index_document_chunks(chunks, metadatas)
    rag.persist()
    return {"file": filename, "chunks_indexed": count}
