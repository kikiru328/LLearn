import anyio
from ulid import ULID
from datetime import datetime, timezone
from user.application.exception import DuplicateEmailError
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.password import Password
from user.infra.repository.user_repo import UserRepository
from utils.crypto import Crypto


class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
        self.ulid = ULID()
        self.crypto = Crypto()

    async def create_user(
        self,
        email: str,
        name: str,
        password: str,
        created_at: datetime | None = None,
    ):
        created_at = created_at or datetime.now(timezone.utc)

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
            created_at=created_at,
            updated_at=created_at,
        )

        await self.user_repo.save(user)
        return user
