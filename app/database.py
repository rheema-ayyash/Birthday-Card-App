import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Database connection URL from environment or local sqlite fallback
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./birthday_card.db"
    )


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
    "check_same_thread": False}
    if "sqlite" in SQLALCHEMY_DATABASE_URL 
    else {},
)

sessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()