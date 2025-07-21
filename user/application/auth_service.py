from datetime import datetime, timezone
import anyio
from fastapi import HTTPException, status
from ulid import ULID
from common.auth import Role, create_access_token
from user.application.exception import DuplicateEmailError
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.password import Password
from user.domain.value_object.role import RoleVO
from utils.crypto import Crypto


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        ulid: ULID = ULID(),
        crypto: Crypto = Crypto(),
    ):

        self.user_repo = user_repo
        self.ulid = ulid
        self.crypto = crypto

    async def signup(
        self,
        email: str,
        name: str,
        password: str,
        created_at: datetime | None = None,
    ):
        created_at = created_at or datetime.now(timezone.utc)

        # validation email exist
        if await self.user_repo.find_by_email(Email(email)):
            raise DuplicateEmailError

        # validation
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
