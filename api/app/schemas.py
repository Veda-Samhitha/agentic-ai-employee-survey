from pydantic import BaseModel, EmailStr
from typing import List, Optional

class LoginIn(BaseModel):
    email: EmailStr
    role: str  # "employee" | "admin"

class SessionOut(BaseModel):
    token: str
    name: str
    role: str

class QuestionIn(BaseModel):
    qtype: str
    text: str

class SurveyCreate(BaseModel):
    title: str
    description: str = ""
    anonymous: bool = True
    questions: List[QuestionIn] = []

class SurveyOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    anonymous: bool = True
    class Config:
        from_attributes = True

class AnswerIn(BaseModel):
    question_id: int
    value_text: Optional[str] = None
    value_numeric: Optional[int] = None
