from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, surveys, responses

app = FastAPI(title="Employee Survey API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],  # dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Routers
app.include_router(auth.router)        # /auth/login
app.include_router(surveys.router)     # /admin/surveys
app.include_router(responses.router)   # /surveys/{id}/questions, /surveys/{id}/responses
