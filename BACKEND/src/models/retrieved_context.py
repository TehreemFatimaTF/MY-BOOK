"""
RetrievedContext model definition
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class RetrievedContextBase(BaseModel):
    query_id: str = Field(..., description="Reference to the original query")
    content_chunk: str = Field(..., min_length=1, description="The text chunk retrieved from the book")
    chunk_id: str = Field(..., description="Identifier for the specific chunk in the book")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Score indicating relevance to the query")

class RetrievedContextCreate(RetrievedContextBase):
    pass

class RetrievedContextUpdate(BaseModel):
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class RetrievedContext(RetrievedContextBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True