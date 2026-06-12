from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine — equivalent of DataSource in Spring
engine = create_engine(DATABASE_URL)

# Session factory — equivalent of EntityManager in Spring
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models — equivalent of @Entity base in JPA
Base = declarative_base()

# Dependency — gives us a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()