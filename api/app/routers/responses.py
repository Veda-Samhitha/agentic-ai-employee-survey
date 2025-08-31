# app/routers/responses.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Body
from pydantic import BaseModel, model_validator
from ..routers.auth import get_current_user

router = APIRouter(tags=["responses"])

class AnswerIn(BaseModel):
    question_id: int
    value_text: Optional[str] = None
    value_numeric: Optional[int] = None

    @model_validator(mode="after")
    def check_values(self):
        if self.value_text is None and self.value_numeric is None:
            raise ValueError("Either value_text or value_numeric must be provided")
        return self


# 👇 keep this at the bottom of responses.py
@router.post("/surveys/{sid}/responses", status_code=201)
def submit_response(
    sid: int,
    items: List[AnswerIn],
    current_user = Depends(get_current_user),
):
    return {
        "survey_id": sid,
        "user": getattr(current_user, "email", "anon"),
        "answers": [it.dict() for it in items]
    }
