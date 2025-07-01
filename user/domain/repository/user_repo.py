from abc import ABCMeta, abstractmethod
from typing import Optional

from user.domain.entity.user import User
from user.domain.value_object.email import Email


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: Email):
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User):
        raise NotImplementedError
