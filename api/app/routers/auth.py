from fastapi import APIRouter
from ..schemas import LoginIn, SessionOut
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=SessionOut)
def login(body: LoginIn):
    name = body.email.split("@")[0] if "@" in body.email else "User"
    return {"token": f"demo-{secrets.token_hex(8)}", "name": name, "role": body.role}
# app/routers/auth.py



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # 🔹 validate token here (decode JWT, lookup user, etc.)
    # For now, return dummy user
    return {"username": "testuser", "email": "test@example.com", "role": "admin"}
