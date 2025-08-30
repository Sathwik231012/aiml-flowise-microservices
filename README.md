# AIML Flowise Microservices

A FastAPI-based microservice that exposes AI/ML functionalities like document upload, embeddings, and Retrieval-Augmented Generation (RAG) Q&A as APIs.
The project is modular with clean separation of routes and services, making it easy to extend with more AI/ML features.

---

## 🚀 Features
- FastAPI backend with automatic Swagger docs (`/docs`)
- Document Upload & Indexing (chunks documents, stores embeddings)
- RAG-based Question Answering (retrieves relevant chunks + generates answer)
- Modular project structure (routes & services)
- Ready for Docker & deployment
- Version controlled on GitHub for easy collaboration

---


## 🛠️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sathwik231012/aiml-flowise-microservices.git
   cd aiml-flowise-microservices
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate venv**
   ```bash
   .\venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Run the Server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

👉 Swagger UI: http://127.0.0.1:8000/docs
👉 ReDoc: http://127.0.0.1:8000/redoc

## Example API Usage

### 1. Upload Document

**POST ```/docs/upload```**

```bash
curl -X POST "http://127.0.0.1:8000/docs/upload" -F "file=@sample.txt"
```

**Response:**

```json
{
  "file": "sample.txt",
  "chunks_indexed": 3
}
```

### 2. Ask Questions (RAG Q&A)

**POST ```/qa/```**

**Request:**

```json
{
  "question": "What is the main conclusion of the document?",
  "top_k": 4
}
```

**Response:**

```json
{
  "answer": "The main conclusion of the document is to keep experiments small and iterate quickly.",
  "sources": [
    {
      "file": "sample.txt",
      "chunk_id": 0,
      "content": "Keep experiments small and iterate quickly..."
    }
  ]
}
```

## Next Steps

- Integrate real LLMs (e.g., OpenAI, HuggingFace models) inside `llm_adapter.py`
- Add more microservices (translation, classification, Q&A)
- Deploy using Docker/GitHub Actions

## Author

### M. Sathwik

B.Tech CSE (AI & ML) 
