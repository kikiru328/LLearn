from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email


class UserRepository(IUserRepository):
    async def save(self, user: User) -> None:
        raise NotImplementedError

    async def find_by_id(self, id: str):
        raise NotImplementedError

    async def find_by_email(self, email: Email):
        raise NotImplementedError
