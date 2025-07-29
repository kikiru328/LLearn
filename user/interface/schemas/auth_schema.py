from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from user.domain.entity.user import User


class SignUpBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=64)


class SignUpResponse(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "SignUpResponse":
        return cls(
            name=str(user.name),
            email=str(user.email),
            created_at=user.created_at,
        )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
