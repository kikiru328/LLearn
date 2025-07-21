from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from user.domain.entity.user import User


class SignUpResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    role: str
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "SignUpResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
            created_at=user.created_at,
        )


class SignUpBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=64)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
