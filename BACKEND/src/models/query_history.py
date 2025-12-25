"""
QueryHistory model definition
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class QueryHistoryBase(BaseModel):
    query_id: str = Field(..., description="Reference to the original query")
    user_id: Optional[str] = Field(None, description="Identifier for the user (if available)")
    query_text: str = Field(..., min_length=1, max_length=2000, description="The original query text")
    response_text: str = Field(..., min_length=1, description="The AI-generated response")
    accuracy_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Accuracy rating of the response")
    feedback: Optional[str] = Field(None, max_length=5000, description="User feedback on the response")

class QueryHistoryCreate(QueryHistoryBase):
    pass

class QueryHistoryUpdate(BaseModel):
    accuracy_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    feedback: Optional[str] = Field(None, max_length=5000)

class QueryHistory(QueryHistoryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True