from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteReturn(NoteCreate):
    id: int
    updated_at: datetime
    created_at: datetime
    is_archived: Optional[bool] = False

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] 