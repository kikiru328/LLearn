from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field

from user.domain.entity.user import User
from user.domain.value_object.role import RoleVO


class UpdateUserBody(BaseModel):
    name: str | None = None
    password: str | None = None


class UpdateUserResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    role: str
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UpdateUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
            updated_at=user.updated_at,
        )


class UserResponse(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    role: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
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


class UpdateUserRoleBody(BaseModel):
    role: RoleVO
