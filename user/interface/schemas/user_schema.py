from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field

from user.domain.entity.user import User


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=64)


class CreateUserResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "CreateUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            created_at=user.created_at,
        )


class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=64, default=None)


class UpdateUserResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UpdateUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            updated_at=user.updated_at,
        )


class UserResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class GetUsersPageResponse(BaseModel):
    total_count: int
    page: int
    items_per_page: int
    users: List[UserResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        users: List[UserResponse],
    ) -> "GetUsersPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            users=users,
        )
