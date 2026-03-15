from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine is the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal is what we use to talk to the DB in each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what all our models will inherit from
Base = declarative_base()

# This gives each endpoint its own DB session and closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()