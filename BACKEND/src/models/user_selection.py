"""
UserSelection model definition
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserSelectionBase(BaseModel):
    query_id: str = Field(..., description="Reference to the associated query")
    selected_text: str = Field(..., min_length=1, max_length=5000, description="The text selected by the user")
    selection_metadata: Optional[dict] = Field(None, description="Additional metadata about the selection (position, length, etc.)")

class UserSelectionCreate(UserSelectionBase):
    pass

class UserSelectionUpdate(BaseModel):
    selection_metadata: Optional[dict] = Field(None)

class UserSelection(UserSelectionBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
