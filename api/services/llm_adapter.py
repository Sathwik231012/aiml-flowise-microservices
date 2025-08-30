# api/services/llm_adapter.py
import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv

# load .env from project root
load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "openrouter").lower()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# --- low-level callers ---
def _call_openrouter_chat(messages, temperature: float = 0.2, max_tokens: int = 512) -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set in environment.")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",   # free / fast model on OpenRouter
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    # typical shape: choices[0].message.content
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        # fallback: try common keys
        return data.get("output") or data.get("completion") or json.dumps(data)

def _call_ollama(prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
    url = f"{OLLAMA_HOST}/v1/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "temperature": temperature, "max_tokens": max_tokens}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("completion") or data.get("text") or json.dumps(data)

# --- public generate ---
def generate(prompt: str, temperature: float = 0.2, max_tokens: int = 512, system: Optional[str]=None) -> str:
    """
    Generic generate function. Uses OpenRouter chat completions by default.
    If system is provided, it is sent as the system message.
    """
    try:
        if LLM_BACKEND == "ollama":
            return _call_ollama(prompt, temperature, max_tokens)

        # default: openrouter chat
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return _call_openrouter_chat(messages, temperature, max_tokens)

    except Exception as e:
        return f"LLM call error: {e}"

# --- convenience wrappers used by routes ---

def summarize_text(text: str) -> str:
    """
    Summarize input text concisely.
    """
    system = "You are a concise summarizer. Return a short summary (2-4 sentences). No code blocks."
    prompt = f"Summarize the following text:\n\n{text}"
    return generate(prompt, temperature=0.1, max_tokens=400, system=system)

def answer_question(question: str, context: str) -> str:
    """
    Answer the question using only the provided context.
    """
    system = "You are an assistant. Use ONLY the context to answer. If the answer is not present, reply: 'I don't know.' Keep it short."
    prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}\n\nAnswer:"
    return generate(prompt, temperature=0.0, max_tokens=300, system=system)

def suggest_learning_path(topic: str, level: str, time_per_week: Optional[int]=None, duration_weeks: Optional[int]=None, goal: Optional[str]=None) -> str:
    """
    Suggest a structured learning path. Returns a JSON string describing weeks and tasks.
    """
    system = (
        "You are an expert curriculum designer. Produce ONLY valid JSON in this shape:\n"
        '{"weeks":[{"week":int,"outcome":str,"resources":[str],"tasks":[str]}], "final_project": str}\n'
        "Do not include explanatory text—only JSON."
    )
    extras = []
    if time_per_week:
        extras.append(f"time_per_week: {time_per_week} hours")
    if duration_weeks:
        extras.append(f"duration_weeks: {duration_weeks}")
    if goal:
        extras.append(f"goal: {goal}")
    extra_text = ("; ".join(extras) + ".") if extras else ""
    prompt = f"Create a learning path for topic: '{topic}' at level: '{level}'. {extra_text} Return JSON as described."
    return generate(prompt, temperature=0.3, max_tokens=800, system=system)
