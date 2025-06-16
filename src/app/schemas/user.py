from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

class UpdateUserRequest(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=30)

class UpdateUserResponse(BaseModel):
    id: UUID
    nickname: str
    updated_at: datetime