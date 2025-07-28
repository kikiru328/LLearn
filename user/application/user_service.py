import anyio
from ulid import ULID
from datetime import datetime, timezone

from user.application.exception import UserNotFoundError
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository

from user.domain.value_object.name import Name
from user.domain.value_object.password import Password

from user.domain.value_object.role import RoleVO
from utils.crypto import Crypto


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        ulid: ULID = ULID(),
        crypto: Crypto = Crypto(),
    ):

        self.user_repo = user_repo
        self.ulid = ulid
        self.crypto = crypto

    async def get_user_by_id(
        self,
        user_id: str,
    ):

        user = await self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"user with id={user_id} not found")
        return user

    async def update_user(
        self,
        user_id: str,
        name: str | None = None,
        password: str | None = None,
    ) -> User:

        user = await self.user_repo.find_by_id(id=user_id)

        if user is None:
            raise UserNotFoundError(f"{user_id} user not found")

        updated_at = datetime.now(timezone.utc)

        if name:
            user.name = Name(name)
            user.updated_at = updated_at

        if password:

            # validation
            Password(password)

            # hash
            new_hashed_password = await anyio.to_thread.run_sync(
                self.crypto.encrypt, password
            )

            # VO
            user.password = Password(new_hashed_password)
            user.updated_at = updated_at

        await self.user_repo.update(user)
        return user

    async def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = await self.user_repo.find_users(page, items_per_page)
        return users

    async def delete_user(self, user_id: str) -> None:
        await self.user_repo.delete(user_id)

    async def change_role(self, user_id: str, role: RoleVO) -> User:
        user = await self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"{user_id} not found")

        user.role = role
        user.updated_at = datetime.now(timezone.utc)
        await self.user_repo.update(user)
        return user
