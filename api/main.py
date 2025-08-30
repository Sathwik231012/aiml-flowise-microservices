from fastapi import FastAPI
from api.routes import summarize, qa, learning_path

app = FastAPI(title="AI/ML + Flowise Microservices")

app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(qa.router, prefix="/qa", tags=["Q&A"])
app.include_router(learning_path.router, prefix="/learning-path", tags=["Learning Path"])
