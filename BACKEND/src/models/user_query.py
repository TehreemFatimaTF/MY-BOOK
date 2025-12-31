"""
UserQuery model definition
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserQueryBase(BaseModel):
    book_id: str = Field(..., description="Reference to the book being queried")
    query_text: str = Field(..., min_length=1, max_length=2000, description="The text of the user's query")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Text selected by user for focused queries")
    session_id: Optional[str] = Field(None, description="Session identifier for grouping related queries")

class UserQueryCreate(UserQueryBase):
    pass

class UserQueryUpdate(BaseModel):
    query_text: Optional[str] = Field(None, min_length=1, max_length=2000)
    selected_text: Optional[str] = Field(None, max_length=5000)

class UserQuery(UserQueryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_embedding: Optional[list] = Field(None, description="Vector embedding of the query")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
