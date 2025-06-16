from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class LikeCreateRequest(BaseModel):
    target_type: Literal["summary", "curriculum"]
    target_id: UUID

class LikeDeleteRequest(BaseModel):
    target_type: Literal["summary", "curriculum"]
    target_id: UUID

class LikeResponse(BaseModel):
    id: UUID
    user_id: UUID
    target_type: str
    target_id: UUID
    created_at: datetime