from sqlalchemy import text
from app.db import engine

with engine.connect() as conn:
    version = conn.execute(text("SELECT version();")).fetchone()
    print("Connected! ✅ PostgreSQL version:", version[0])
