from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password


class UserRepository(ABC):
    """User repository interface"""
    @abstractmethod
    async def save(self, user: User) -> User:
        """사용자 저장 (생성/수정)"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """ID로 사용자 조회"""
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """이메일로 사용자 조회 (로그인 시 사용)"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """이메일 중복 체크"""
        pass

    @abstractmethod
    async def update_password(self, user_id: UUID, new_password: Password) -> None:
        """비밀번호 변경"""
        pass