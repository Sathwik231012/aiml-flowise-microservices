# api/services/embeddings.py
from typing import List
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        # small, fast model good for RAG
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Return list of vectors (Python lists) for the given list of texts.
    """
    model = get_model()
    vectors = model.encode(texts, show_progress_bar=False)
    # convert numpy arrays to native python lists for Chroma
    return [v.tolist() for v in vectors]
