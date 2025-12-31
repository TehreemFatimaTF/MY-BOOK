"""
Database schema definitions for the Book RAG Chatbot
"""

# This file would contain SQLAlchemy models or other database schema definitions
# For now, we'll create a placeholder that will be expanded as we implement the models

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class BookContent(Base):
    __tablename__ = "book_content"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String, nullable=False)
    chunked_content = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
