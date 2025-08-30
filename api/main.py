# api/main.py
from fastapi import FastAPI
from api.routes import summarize, qa, learning_path
from api.routes import docs_upload  # import the docs upload router

app = FastAPI(title="AI/ML + Flowise Microservices")

app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(qa.router, prefix="/qa", tags=["Q&A"])
app.include_router(docs_upload.router, prefix="/docs", tags=["Docs"])
app.include_router(learning_path.router, prefix="/learning-path", tags=["Learning Path"])

@app.get("/")
def root():
    return {"status": "ok", "message": "AI/ML microservices running"}
