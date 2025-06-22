from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from domain.value_objects.email import Email
from domain.value_objects.password import Password

@dataclass
class User:
    """User's domain entity"""
    id: UUID
    email: Email
    nickname: str
    hashed_password: Password
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_admin: bool = False
    
    def change_nickname(self, new_nickname: str) -> None:
        """Change User's nickname to new_nickname"""
        if not new_nickname or len(new_nickname.strip()) < 2:
            raise ValueError("닉네임은 2자 이상이어야 합니다.")
        self.nickname = new_nickname.strip()
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """soft delete, 계정 비활성화"""
        self.is_active = False
        self.updated_at = datetime.now()