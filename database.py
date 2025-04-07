from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CodeReview(Base):
    __tablename__ = 'code_reviews'

    id = Column(Integer, primary_key=True)
    uploaded_code = Column(Text, nullable=False)
    suggestions = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database connection
engine = create_engine('sqlite:///code_reviews.db')  # Use your chosen database name
Base.metadata.create_all(engine)

# Session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
