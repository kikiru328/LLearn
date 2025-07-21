from datetime import datetime
from pydantic import BaseModel

from user.domain.entity.user import User


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


class CreateUserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "CreateUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            created_at=user.created_at,
        )
