"""
GeneratedResponse model definition
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class GeneratedResponseBase(BaseModel):
    query_id: str = Field(..., description="Reference to the original query")
    response_text: str = Field(..., min_length=1, description="The text of the AI-generated response")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence level in the response")
    source_chunks: Optional[List[str]] = Field(None, description="IDs of the chunks used to generate the response")

class GeneratedResponseCreate(GeneratedResponseBase):
    pass

class GeneratedResponseUpdate(BaseModel):
    response_text: Optional[str] = Field(None, min_length=1)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class GeneratedResponse(GeneratedResponseBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True