# AIML Flowise Microservices

A FastAPI-based microservice that exposes AI/ML functionalities (like text summarization) as APIs.  
This project is modular, with clean separation of routes and services, and is ready to be extended.

---

## 🚀 Features
- FastAPI backend with automatic Swagger docs (`/docs`)
- Modular project structure (routes & services)
- Example AI/ML service: Text Summarization (stubbed, extendable to real LLMs)
- Easy deployment with Uvicorn
- Ready for GitHub versioning

---

## 📂 Project Structure

aiml-flowise-microservices/
│── api/

│ ├── main.py # FastAPI entrypoint

│ ├── routes/ # API route handlers

│ │ └── summarize.py

│ └── services/ # Business logic / LLM integration

│ └── llm_adapter.py

│

│── requirements.txt # Python dependencies

│── README.md # Project documentation

│── .gitignore # Ignore venv, cache, etc.

│── venv/ (ignored) # Local virtual environment


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

### POST ```/summarize/```

**Request:**

```json
{
  "text": "Artificial intelligence is transforming industries..."
}
```

**Response:**

```json
{
  "summary": "This is a short summary."
}
```

## Next Steps

- Integrate real LLMs (e.g., OpenAI, HuggingFace models) inside `llm_adapter.py`
- Add more microservices (translation, classification, Q&A)
- Deploy using Docker/GitHub Actions

## Author

### M. Sathwik

B.Tech CSE (AI & ML) 
