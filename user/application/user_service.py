from ulid import ULID
from datetime import datetime, timezone
from user.application.exception import DuplicateEmailError
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.password import Password
from utils.crypto import Crypto


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        crypto: Crypto,
    ):
        self.user_repo = user_repo
        self.crypto = crypto

    def create_user(
        self,
        email: str,
        name: str,
        password: str,
        created_at: datetime | None = None,
    ):
        created_at = created_at or datetime.now(timezone.utc)

        # duplicate?
        if self.user_repo.find_by_email(Email(email)):
            raise DuplicateEmailError

        Password(password)
        hashed_password = self.crypto.encrypt(password)

        user = User(
            id=ULID().generate(),
            email=Email(email),
            name=Name(name),
            password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
        )

        self.user_repo.save(user)
        return user
