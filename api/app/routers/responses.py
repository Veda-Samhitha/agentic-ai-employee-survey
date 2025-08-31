from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/surveys", tags=["responses"])

@router.get("/{sid}/questions")
def get_questions(sid: int, db: Session = Depends(get_db)):
    qs = db.query(models.Question).filter(models.Question.survey_id == sid).all()
    if not qs:
        exists = db.query(models.Survey).filter(models.Survey.id == sid).first()
        if not exists:
            raise HTTPException(404, "Survey not found")
    return [{"id": q.id, "qtype": q.qtype, "text": q.text} for q in qs]

@router.post("/{sid}/responses")
def submit_response(sid: int, payload: list[schemas.AnswerIn], db: Session = Depends(get_db)):
    # (Phase 2: no real auth yet) use dummy user_id=1
    if not db.query(models.Survey).filter(models.Survey.id == sid).first():
        raise HTTPException(404, "Survey not found")

    r = models.Response(survey_id=sid, user_id=1)
    db.add(r); db.flush()
    for a in payload:
        db.add(models.Answer(
            response_id=r.id,
            question_id=a.question_id,
            value_text=a.value_text,
            value_numeric=a.value_numeric
        ))
    db.commit()
    return {"ok": True, "response_id": r.id}
