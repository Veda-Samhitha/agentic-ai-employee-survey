# app/seed.py
"""
Idempotent seed script for local dev.

Run from the repo's api/ folder:
    python -m app.create_tables
    python -m app.seed
"""

from datetime import datetime
from typing import Any, Iterable, Optional

from app.db import SessionLocal  # absolute import (fixes ImportError from relative paths)


# ----------------------------- model resolution -----------------------------

def resolve_models():
    """
    Prefer models from app.models (single module file).
    Fallback to app.db if models are defined there.
    """
    tried = []
    mod = None
    try:
        import app.models as mod  # pragma: no cover
    except Exception as e:
        tried.append(("app.models", repr(e)))
        mod = None

    if mod is None:
        try:
            import app.db as mod  # pragma: no cover
        except Exception as e:
            tried.append(("app.db", repr(e)))
            mod = None

    if mod is None:
        print("❌ Could not import a module that defines your models. Tried:")
        for p, e in tried:
            print(f"   - {p}: {e}")
        raise SystemExit(1)

    def need(name: str):
        cls = getattr(mod, name, None)
        if cls is None:
            raise RuntimeError(
                f"Model {name} not found in {mod.__name__}. "
                f"Define it there or update seed.py to your paths."
            )
        return cls

    return {
        "User": need("User"),
        "Survey": need("Survey"),
        "Question": need("Question"),
        # Optional models (skip gracefully if absent)
        "Response": getattr(mod, "Response", None),
        "Answer": getattr(mod, "Answer", None),
    }


MODELS = resolve_models()
User = MODELS["User"]
Survey = MODELS["Survey"]
Question = MODELS["Question"]
Response = MODELS["Response"]
Answer = MODELS["Answer"]


# ------------------------------- tiny helpers -------------------------------

def set_first_attr(obj: Any, candidates: Iterable[str], value: Any) -> bool:
    """Set the first attribute that exists on obj from candidates to value. Returns True if set."""
    for name in candidates:
        if hasattr(obj, name):
            setattr(obj, name, value)
            return True
    return False


def get_first_attr(obj: Any, candidates: Iterable[str]) -> Optional[Any]:
    """Return the first existing attribute value on obj from candidates."""
    for name in candidates:
        if hasattr(obj, name):
            return getattr(obj, name)
    return None


def col(model, *names):
    """Return the first existing ORM column on a model (safe lookup)."""
    for name in names:
        if hasattr(model, name):
            return getattr(model, name)
    raise AttributeError(f"{model.__name__} has none of: {names}")


def ensure_password_fields(user_obj: Any, plain_password: str) -> None:
    """
    Try to hash password using a project helper if available.
    - Looks for app.security.get_password_hash or app.core.security.get_password_hash dynamically.
    - Falls back to setting a plain password if your model has a 'password' field.
    """
    import importlib

    hasher = None
    for modname in ("app.security", "app.core.security"):
        try:
            mod = importlib.import_module(modname)
            if hasattr(mod, "get_password_hash"):
                hasher = getattr(mod, "get_password_hash")
                break
        except Exception:
            continue

    if hasher:
        hashed = hasher(plain_password)
        # Most projects store hashed_password/password_hash; use 'password' as very last resort.
        if not set_first_attr(user_obj, ("hashed_password", "password_hash", "password"), hashed):
            set_first_attr(user_obj, ("password",), plain_password)  # last resort
    else:
        # No hasher in project: keep it simple for dev; if your login requires hashing,
        # add app/security.py with get_password_hash (see earlier instructions).
        if not set_first_attr(user_obj, ("hashed_password", "password_hash"), None):
            set_first_attr(user_obj, ("password",), plain_password)


# ---------------------------------- seed ------------------------------------

def seed():
    db = SessionLocal()
    try:
        # ---- Users (admin + normal) ----
        admin_email = "admin@example.com"
        user_email = "user@example.com"

        admin = db.query(User).filter_by(email=admin_email).one_or_none()
        if not admin:
            admin = User()
            set_first_attr(admin, ("email",), admin_email)
            set_first_attr(admin, ("name", "full_name", "username"), "Admin")
            set_first_attr(admin, ("is_admin", "is_superuser", "is_staff"), True)
            ensure_password_fields(admin, "Admin@123")
            db.add(admin)
            db.flush()
            print("→ Created admin user")

        user = db.query(User).filter_by(email=user_email).one_or_none()
        if not user:
            user = User()
            set_first_attr(user, ("email",), user_email)
            set_first_attr(user, ("name", "full_name", "username"), "Demo User")
            set_first_attr(user, ("is_admin", "is_superuser", "is_staff"), False)
            ensure_password_fields(user, "User@123")
            db.add(user)
            db.flush()
            print("→ Created demo user")

        # ---- Surveys + Questions ----
        def get_or_create_survey(title: str, description: str, creator_id: Optional[int]) -> Any:
            existing = db.query(Survey).filter_by(title=title).one_or_none()
            if existing:
                return existing
            s = Survey()
            set_first_attr(s, ("title",), title)
            set_first_attr(s, ("description", "details", "summary"), description)
            set_first_attr(s, ("is_active", "active", "enabled"), True)
            # created_by variants (id field preferred; relationship as fallback)
            if creator_id is not None:
                if not set_first_attr(s, ("created_by_id", "creator_id", "owner_id"), creator_id):
                    set_first_attr(s, ("created_by", "creator", "owner"), creator_id)
            db.add(s)
            db.flush()
            print(f"→ Created survey: {title}")
            return s

        def add_question(survey_obj: Any, text: str, qtype: str = "text", options: Optional[list] = None) -> Any:
            survey_id_val = get_first_attr(survey_obj, ("id", "survey_id"))
            survey_col = col(Question, "survey_id", "surveyId", "surveyID")
            text_col = col(Question, "text", "question_text", "label")

            existing = (
                db.query(Question)
                .filter(survey_col == survey_id_val, text_col == text)
                .one_or_none()
            )

            if existing:
                return existing

            q = Question()
            # Link to survey
            if not set_first_attr(q, ("survey_id", "surveyId", "surveyID"), survey_id_val):
                set_first_attr(q, ("survey",), survey_obj)

            set_first_attr(q, ("text", "question_text", "label"), text)
            set_first_attr(q, ("type", "q_type", "kind"), qtype)
            if options:
                set_first_attr(q, ("options", "choices", "metadata"), options)

            db.add(q)
            db.flush()
            print(f"   → Added Q: {text}")
            return q

        admin_id = get_first_attr(admin, ("id",))
        s1 = get_or_create_survey(
            "Employee Engagement Pulse",
            "Quick 5-question pulse to gauge engagement and blockers.",
            admin_id,
        )
        s2 = get_or_create_survey(
            "Work–Life Balance Check",
            "How balanced is your workload, energy, and recovery?",
            admin_id,
        )

        # Questions for survey 1
        for text, qtype, opts in [
            ("I feel motivated to do my best at work.", "rating", None),
            ("Top blocker this week?", "text", None),
            ("Would you recommend our team as a great place to work?", "single_choice", ["Yes", "No", "Maybe"]),
        ]:
            add_question(s1, text, qtype, opts)

        # Questions for survey 2
        for text, qtype, opts in [
            ("Weekly hours typically worked", "number", None),
            ("How often can you fully disconnect after work?", "single_choice", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
            ("One change that would improve your balance", "text", None),
        ]:
            add_question(s2, text, qtype, opts)

        # ---- Optional: one sample response + answer (skip gracefully if models missing) ----
        if Response is not None:
            s1_id = get_first_attr(s1, ("id",))
            # find a question from s1
            survey_col_q = col(Question, "survey_id", "surveyId", "surveyID")
            q1 = db.query(Question).filter(survey_col_q == s1_id).first()

            survey_col_r = col(Response, "survey_id", "surveyId")
            user_col_r = col(Response, "user_id", "userId")

            existing_resp = (
                db.query(Response)
                .filter(
                    survey_col_r == s1_id,
                    user_col_r == get_first_attr(user, ("id",)),
                )
                .one_or_none()
            )

            if not existing_resp:
                r = Response()
                set_first_attr(r, ("survey_id", "surveyId"), s1_id)
                set_first_attr(r, ("user_id", "userId"), get_first_attr(user, ("id",)))
                set_first_attr(r, ("submitted_at", "created_at", "timestamp"), datetime.utcnow())
                db.add(r)
                db.flush()
                print("→ Created sample response for 'Employee Engagement Pulse'")

                if Answer is not None and q1 is not None:
                    a = Answer()
                    set_first_attr(a, ("response_id", "responseId"), get_first_attr(r, ("id",)))
                    set_first_attr(a, ("question_id", "questionId"), get_first_attr(q1, ("id",)))
                    set_first_attr(a, ("value", "text", "answer", "choice"), "4")
                    db.add(a)
                    db.flush()
                    print("   → Added one sample answer")
            else:
                print("↷ Sample response already exists; skipping")

        db.commit()
        print("\n✅ Seed complete.")
        print("Users:")
        print("  - admin: admin@example.com / Admin@123")
        print("  - user : user@example.com / User@123")
    except Exception as e:
        db.rollback()
        print("❌ Seed failed:", repr(e))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
