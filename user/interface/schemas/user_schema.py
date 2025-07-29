from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field

from user.domain.entity.user import User
from user.domain.value_object.role import RoleVO


class GetUserResponse(BaseModel):
    """Response for USER role"""

    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)

    @classmethod
    def from_domain(cls, user: User) -> "GetUserResponse":
        return cls(
            name=str(user.name),
            email=str(user.email),
        )


class UpdateUserBody(BaseModel):
    name: str | None = None
    password: str | None = None


class UpdateUserResponse(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UpdateUserResponse":
        return cls(
            name=str(user.name),
            email=str(user.email),
            updated_at=user.updated_at,
        )


class GetUsersPageResponse(BaseModel):
    "Response USER List for USER role"

    total_count: int
    page: int
    items_per_page: int
    users: List[GetUserResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        users: List[GetUserResponse],
    ) -> "GetUsersPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            users=users,
        )


class UpdateUserRoleBody(BaseModel):
    role: RoleVO
