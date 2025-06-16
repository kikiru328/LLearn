from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CommentCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentUpdateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentResponse(BaseModel):
    id: UUID
    user_id: UUID
    summary_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime