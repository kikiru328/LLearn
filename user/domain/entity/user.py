from dataclasses import dataclass
from datetime import datetime

from user.domain.value_object.email import Email
from user.domain.value_object.name import Name


@dataclass
class User:
    id: str
    email: Email
    name: Name
    password: str
    created_at: datetime
    updated_at: datetime
