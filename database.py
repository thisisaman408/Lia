from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Loading env variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/liaplus_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes the database and runs migrations."""
    # Create Tables
    Base.metadata.create_all(bind=engine)
    
    # Auto-Migration for new columns (SRP: encapsulated here)
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE conversations ADD COLUMN IF NOT EXISTS title VARCHAR"))
            conn.execute(text("ALTER TABLE messages ADD COLUMN IF NOT EXISTS corrected_label VARCHAR"))
            conn.commit()
            print("DATABASE: Schema initialized and migrated.")
    except Exception as e:
        print(f"DATABASE MIGRATION WARNING: {e}")
