from dataclasses import dataclass
from datetime import datetime

from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO


@dataclass
class User:
    id: str
    email: Email
    name: Name
    password: str
    role: RoleVO
    created_at: datetime
    updated_at: datetime
