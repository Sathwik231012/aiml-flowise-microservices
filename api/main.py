# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import summarize, qa, docs_upload, learning_path

app = FastAPI(title="AI/ML + Flowise Microservices")

# Origins from which the frontend will be making requests
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add CORS middleware to allow the frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(qa.router, prefix="/qa", tags=["Q&A"])
app.include_router(docs_upload.router, prefix="/docs", tags=["Docs"])
app.include_router(learning_path.router, prefix="/learning-path", tags=["Learning Path"])

@app.get("/")
def root():
    return {"status": "ok", "message": "AI/ML microservices running"}