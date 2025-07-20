from abc import ABCMeta, abstractmethod

from user.domain.entity.user import User
from user.domain.value_object.email import Email


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: Email):
        raise NotImplementedError
