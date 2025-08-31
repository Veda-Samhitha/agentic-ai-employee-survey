from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models, schemas

router = APIRouter(prefix="/admin/surveys", tags=["surveys"])

@router.post("", response_model=schemas.SurveyOut)
def create_survey(data: schemas.SurveyCreate, db: Session = Depends(get_db)):
    s = models.Survey(
        title=data.title,
        description=data.description,
        anonymous=data.anonymous
    )
    db.add(s)
    db.flush()
    for q in data.questions:
        db.add(models.Question(survey_id=s.id, qtype=q.qtype, text=q.text))
    db.commit()
    db.refresh(s)
    return s

@router.get("", response_model=list[schemas.SurveyOut])
def list_surveys(db: Session = Depends(get_db)):
    return db.query(models.Survey).all()
