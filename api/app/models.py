# app/models.py
from sqlalchemy import (
    Column, Integer, DateTime, func, String, Boolean, ForeignKey, Text, UniqueConstraint
)
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="employee")
    name = Column(String)


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text, default="")
    anonymous = Column(Boolean, default=True)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    qtype = Column(String)          # e.g.: "likert" | "text" | "mcq"
    text = Column(Text)


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # add a timestamp with a default so inserts never fail
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    value_text = Column(Text, nullable=True)
    value_numeric = Column(Integer, nullable=True)


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint("survey_id", "user_id", name="uq_assignment"),)
