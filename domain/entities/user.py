from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from domain.value_objects.email import Email
from domain.value_objects.password import Password

@dataclass(kw_only=True)
class User:
    """User's domain entity"""
    id: UUID = field(default_factory= uuid4)
    email: Email
    nickname: str
    hashed_password: Password
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def change_nickname(self, new_nickname: str) -> None:
        """Change User's nickname to new_nickname"""
        if not new_nickname or len(new_nickname.strip()) < 2:
            raise ValueError("닉네임은 2자 이상이어야 합니다.")
        self.nickname = new_nickname.strip()
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """activate"""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """soft delete, 계정 비활성화"""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)