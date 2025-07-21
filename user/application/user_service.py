import anyio
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from ulid import ULID
from datetime import datetime, timezone
from common.auth import Role, create_access_token
from user.application.exception import DuplicateEmailError, UserNotFoundError
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email
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

    async def login(
        self,
        email: str,
        password: str,
    ):
        user = await self.user_repo.find_by_email(Email(email))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not self.crypto.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token(subject=user.id, role=Role(user.role))
        return access_token, user.role

    async def create_user(
        self,
        email: str,
        name: str,
        password: str,
        created_at: datetime | None = None,
    ):

        created_at = created_at or datetime.now(timezone.utc)  # 만들어진 날짜는 자동

        # duplicate?
        if await self.user_repo.find_by_email(Email(email)):
            raise DuplicateEmailError

        Password(password)
        hashed_password = await anyio.to_thread.run_sync(self.crypto.encrypt, password)

        user = User(
            id=self.ulid.generate(),
            email=Email(email),
            name=Name(name),
            password=hashed_password,
            role=RoleVO.USER,
            created_at=created_at,
            updated_at=created_at,
        )

        await self.user_repo.save(user)
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
            if len(password) < 8:
                raise RequestValidationError("password must be at least 8 characters")

            Password(password)
            new_hashed_password = await anyio.to_thread.run_sync(
                self.crypto.encrypt, password
            )
            user.password = new_hashed_password
            user.updated_at = updated_at

        await self.user_repo.update(user)
        return user

    async def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = await self.user_repo.get_users(page, items_per_page)
        return users

    async def delete_user(self, user_id: str):
        await self.user_repo.delete(user_id)
