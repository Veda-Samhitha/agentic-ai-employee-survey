# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import auth, surveys, responses


def _allowed_origins() -> list[str]:
    """
    Read a comma-separated env var ALLOWED_ORIGINS, e.g.:
      https://your-web.vercel.app, http://localhost:5173
    Falls back to local dev origins.
    """
    raw = os.getenv("ALLOWED_ORIGINS")
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    return ["http://localhost:5173", "http://127.0.0.1:5173"]


app = FastAPI(title="Employee Survey API", version="1.0.0")

ALLOWED_ORIGINS = _allowed_origins()

# CORS (credentials allowed only with explicit origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ——— friendly root & health ———
@app.get("/")
def root():
    return {"status": "running", "service": "Employee Survey API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ——— routers ———
app.include_router(auth.router)        # /auth/login
app.include_router(surveys.router)     # /admin/surveys
app.include_router(responses.router)   # /surveys/{sid}/questions, /surveys/{sid}/responses
