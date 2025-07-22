from typing import Optional
import pytest
from datetime import datetime, timezone
from user.application.auth_service import AuthService
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email

from user.application.exception import DuplicateEmailError, UserNotFoundError

# from user.domain.value_object.name import Name
from utils.crypto import Crypto


class InMemoryUserRepo(IUserRepository):
    def __init__(self):
        self._by_id: dict[str, User] = {}
        self._by_email: dict[Email, User] = {}

    async def save(self, user: User) -> None:
        if user.id in self._by_id or user.email in self._by_email:
            raise ValueError("duplicate user")

        self._by_id[user.id] = user
        self._by_email[user.email] = user

    async def find_by_id(self, id: str) -> Optional[User]:
        return self._by_id.get(id)

    async def find_by_email(self, email: Email) -> Optional[User]:
        return self._by_email.get(email)

    async def update(self, user: User) -> None:
        if user.id not in self._by_id:
            raise UserNotFoundError(f"{id} not found")
        self._by_id[user.id] = user
        self._by_email[user.email] = user

    async def get_users(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ):
        total_count = len(self._by_id)
        users = list(self._by_id.values())[
            (page - 1) * items_per_page : page * items_per_page
        ]
        return total_count, users

    async def delete(self, id: str) -> None:
        user = self._by_id.get(id)
        if user is None:
            raise UserNotFoundError(f"{id} not found")
        del self._by_id[id]


pytestmark = pytest.mark.asyncio


async def test_sign_up_sucess():
    user_mock_repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=user_mock_repo, crypto=crypto)
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock_user = await auth_service.signup(
        email="pecan@gmail.com",
        name="피칸",
        password="Aa1!aaaa",
        created_at=now,
    )
    assert await user_mock_repo.find_by_id(mock_user.id) == mock_user
    assert crypto.verify("Aa1!aaaa", mock_user.password)
    assert mock_user.created_at == now and mock_user.updated_at == now
    assert mock_user.id.startswith("01")
    assert mock_user.role == "USER"


async def test_sign_up_duplicate_email():
    user_mock_repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=user_mock_repo, crypto=crypto)

    # 선행 사용자 등록
    await auth_service.signup(
        email="dup@gmail.com",
        name="User1",
        password="Aa1!aaaa",
    )

    with pytest.raises(DuplicateEmailError):
        await auth_service.signup(
            email="dup@gmail.com",
            name="User2",
            password="Bb2@bbbb",
        )


async def test_log_in_success():
    user_mock_repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=user_mock_repo, crypto=crypto)
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    # 선행 사용자 등록
    mock_user = await auth_service.signup(
        email="pecan@gmail.com",
        name="피칸",
        password="Aa1!aaaa",
        created_at=now,
    )

    access_token, role = await auth_service.login(
        email=str(mock_user.email),
        password="Aa1!aaaa",
    )
    assert access_token
    assert mock_user.role == role
