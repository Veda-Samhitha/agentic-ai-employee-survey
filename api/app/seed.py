from .db import get_db, SessionLocal
from . import models

def run():
    db = SessionLocal()
    try:
        # users
        admin = db.query(models.User).filter_by(email="hr@company.com").first()
        if not admin:
            admin = models.User(email="hr@company.com", name="HR Admin", role="admin")
            db.add(admin)

        emp = db.query(models.User).filter_by(email="emp@company.com").first()
        if not emp:
            emp = models.User(email="emp@company.com", name="Employee One", role="employee")
            db.add(emp)

        db.commit()

        # survey 1
        s1 = db.query(models.Survey).filter_by(title="Q2 Employee Satisfaction").first()
        if not s1:
            s1 = models.Survey(title="Q2 Employee Satisfaction", description="Quarterly check-in", anonymous=True)
            db.add(s1); db.flush()
            db.add_all([
                models.Question(survey_id=s1.id, qtype="likert", text="Rate work-life balance"),
                models.Question(survey_id=s1.id, qtype="text", text="Any suggestions?"),
            ])
            db.add(models.Assignment(survey_id=s1.id, user_id=emp.id, is_completed=False))

        # survey 2
        s2 = db.query(models.Survey).filter_by(title="Remote Work Feedback").first()
        if not s2:
            s2 = models.Survey(title="Remote Work Feedback", description="Tools & process", anonymous=True)
            db.add(s2); db.flush()
            db.add_all([
                models.Question(survey_id=s2.id, qtype="likert", text="How satisfied are you with remote tools?"),
                models.Question(survey_id=s2.id, qtype="text", text="What could be improved?"),
            ])
            db.add(models.Assignment(survey_id=s2.id, user_id=emp.id, is_completed=False))

        db.commit()
        print("Seeded ✅")
    finally:
        db.close()

if __name__ == "__main__":
    run()
