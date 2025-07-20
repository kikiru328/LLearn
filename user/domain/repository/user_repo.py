from abc import ABCMeta, abstractmethod

from user.domain.entity.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: str):
        pass

    @abstractmethod
    def find_by_email(self, email: str):
        pass
