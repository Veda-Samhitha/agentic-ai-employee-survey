# app/patch_submitted_at.py
from sqlalchemy import text
from app.db import engine

SQL = """
ALTER TABLE responses
  ADD COLUMN IF NOT EXISTS submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
"""

if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text(SQL))
    print("✅ responses.submitted_at ensured in DB (NOT NULL, DEFAULT NOW()).")
