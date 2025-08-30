# api/services/rag.py
import os
from typing import List, Tuple, Dict, Any
from .embeddings import embed_texts

import chromadb

PERSIST_DIR = os.getenv("VECTOR_DB_DIR", "./chroma_db")
COLLECTION_NAME = "documents"

_client = None
_collection = None

def _init_client():
    global _client, _collection
    if _client is not None and _collection is not None:
        return _client, _collection

    # Try persistent Settings style first, else fallback to in-memory client
    try:
        from chromadb.config import Settings
        settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR)
        _client = chromadb.Client(settings)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
        return _client, _collection
    except Exception:
        try:
            _client = chromadb.Client()
            if hasattr(_client, "get_or_create_collection"):
                _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
            else:
                try:
                    _collection = _client.create_collection(name=COLLECTION_NAME)
                except Exception:
                    _collection = _client.get_collection(name=COLLECTION_NAME)
            return _client, _collection
        except Exception as e:
            raise RuntimeError(f"Failed to initialize chroma client: {e}")

def index_document_chunks(chunks: List[str], metadatas: List[Dict[str, Any]]) -> int:
    """
    Add chunks to the vector DB. Return number of chunks added.
    """
    if not chunks:
        return 0
    client, collection = _init_client()
    vectors = embed_texts(chunks)

    # Build stable ids for each chunk (required by some chroma versions)
    ids = []
    for meta in metadatas:
        fname = meta.get("file", "file")
        cid = meta.get("chunk_id")
        ids.append(f"{fname}__chunk__{cid}")

    # Try adding with ids (newer chroma), fall back to older signature if necessary
    try:
        collection.add(ids=ids, documents=chunks, metadatas=metadatas, embeddings=vectors)
    except TypeError:
        # older chroma versions may not accept ids keyword
        try:
            collection.add(documents=chunks, metadatas=metadatas, embeddings=vectors)
        except Exception as e:
            raise
    return len(chunks)

def retrieve(query: str, top_k: int = 4) -> List[Tuple[str, Dict[str, Any], float]]:
    client, collection = _init_client()
    qvecs = embed_texts([query])
    res = collection.query(query_embeddings=qvecs, n_results=top_k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    results = []
    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        dist = dists[i] if i < len(dists) else 0.0
        results.append((doc, meta, float(dist)))
    return results

def persist():
    try:
        client, _ = _init_client()
        if hasattr(client, "persist"):
            client.persist()
    except Exception:
        pass
