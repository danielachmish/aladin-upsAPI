import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# קח את כתובת הדאטאבייס מהסביבה – Render תכניס אוטומטית את DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:020796@localhost/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()