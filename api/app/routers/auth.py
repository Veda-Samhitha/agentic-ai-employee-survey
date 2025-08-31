from fastapi import APIRouter
from ..schemas import LoginIn, SessionOut
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=SessionOut)
def login(body: LoginIn):
    name = body.email.split("@")[0] if "@" in body.email else "User"
    return {"token": f"demo-{secrets.token_hex(8)}", "name": name, "role": body.role}
