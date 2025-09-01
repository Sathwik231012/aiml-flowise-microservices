# AIML Flowise Microservices

A FastAPI-based microservice that exposes AI/ML functionalities like document upload, embeddings, and Retrieval-Augmented Generation (RAG) Q&A as APIs. The project is modular with a clean separation of routes and services, making it easy to extend with more AI/ML features.

---

## Submission Checklist
- [x] Code hosted on GitHub.
- [x] All three required endpoints are implemented:
  - `/summarize`
  - `/qa` (with RAG document upload via `/docs/upload`)
  - `/learning-path`
- [x] Application uses an open-source LLM backend (OpenRouter).
- [x] A Postman collection is included in the `postman/` directory for easy testing.
- [x] README includes full setup and usage instructions.

---

## 🚀 Features
- **FastAPI Backend:** Provides automatic interactive API documentation (Swagger UI) at `/docs`.
- **Document Upload & Indexing:** Endpoint to upload `.pdf` and `.txt` files, which are then chunked and stored as vector embeddings.
- **RAG-based Question Answering:** Retrieves relevant document chunks to answer user questions based on the uploaded content.
- **Modular Project Structure:** Clean separation of concerns between API routes and backend services.
- **Docker Ready:** Includes a `Dockerfile` for easy containerization and deployment.
- **Version Controlled:** Managed with Git on GitHub for easy collaboration.

---

## 🛠️ Setup and Run

**Prerequisites:**
*   Python 3.10+
*   An API key from [OpenRouter.ai](https://openrouter.ai/keys)


1. **Clone the repository**
   ```bash
   git clone https://github.com/Sathwik231012/aiml-flowise-microservices.git
   cd aiml-flowise-microservices
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```


3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Step 4: Configure Environment Variables**
   ```bash
   copy .env.example .env
   notepad .env
   ```
   Inside the `.env` file, set your `OPENROUTER_API_KEY`.

## Run the Server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

👉 Swagger UI: http://127.0.0.1:8000/docs

👉 ReDoc: http://127.0.0.1:8000/redoc


## Example API Usage - Postman

### 1. Import the Collection

- Open your Postman desktop app.
- Click Import -> File -> Upload Files.
- Select the postman/collection.json file from this repository.
- A new collection named "AIML Microservices - OneVarsity" will appear.

### 2. Configure Collection Variables

- Click on the collection and select the Variables tab.
- Update the **CURRENT VALUE** for the `filePath` variable to be the full, absolute path to a sample `.txt` or `.pdf` file on your computer.

### 3.Run the API Requests (In Order)

1. **Upload Document:** Select this request and click Send. This will upload and index your file.
2. **Ask a Question (RAG):** Select this request and click Send. It will ask a question about the document you just uploaded.
3. **Summarize Text:** Select this request to test the summarization endpoint.


## Next Steps

- Integrate real LLMs (e.g., OpenAI, HuggingFace models) inside `llm_adapter.py`
- Add more microservices (translation, classification, Q&A)
- Deploy using Docker/GitHub Actions

## Author

### M. Sathwik

B.Tech CSE (AI & ML) 
