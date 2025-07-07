from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="이메일")
    nickname: str = Field(..., min_length=2, max_length=10, description="닉네임")
    password: str = Field(..., min_length=8, description="비밀번호")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., description="비밀번호")


class UpdateUserRequest(BaseModel):
    nickname: Optional[str] = Field(
        None, min_length=2, max_length=10, description="닉네임"
    )


class UserResponse(BaseModel):
    id: UUID
    email: str
    nickname: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
