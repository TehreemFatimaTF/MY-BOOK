"""
BookContent model definition
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class BookContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=200, description="Author of the book")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN of the book")
    content: str = Field(..., min_length=100, description="Full text content of the book")

class BookContentCreate(BookContentBase):
    pass

class BookContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    content: Optional[str] = Field(None, min_length=100)

class BookContent(BookContentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_hash: str = Field(..., description="Hash of the content for change detection")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="processing", description="Processing status: processing, ready, failed")
    
    class Config:
        from_attributes = True