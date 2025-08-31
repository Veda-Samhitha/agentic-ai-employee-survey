from .db import Base, engine
# import models so SQLAlchemy sees the tables
from . import models  # noqa: F401

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
