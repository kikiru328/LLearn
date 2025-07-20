import pytest
from datetime import datetime, timezone
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email

from user.application.user_service import UserService
from user.application.exception import DuplicateEmailError

from utils.crypto import Crypto


class InMemoryUserRepo(IUserRepository):
    def __init__(self):
        self._by_id: dict[str, User] = {}
        self._by_email: dict[Email, User] = {}

    def save(self, user: User):
        if user.id in self._by_id or user.email in self._by_email:
            raise ValueError("duplicate user")

        self._by_id[user.id] = user
        self._by_email[user.email] = user

    def find_by_id(self, id: str):
        return self._by_id.get(id)

    def find_by_email(self, email: Email):
        return self._by_email.get(email)


def test_create_user_sucess():
    user_mock_repo = InMemoryUserRepo()
    crypto = Crypto()

    user_service = UserService(user_mock_repo, crypto)

    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock_user = user_service.create_user(
        email="pecan@gmail.com",
        name="피칸",
        password="Aa1!aaaa",
        created_at=now,
    )

    assert user_mock_repo.find_by_id(mock_user.id) == mock_user
    assert crypto.verify("Aa1!aaaa", mock_user.password)
    assert mock_user.created_at == now and mock_user.updated_at == now
    assert mock_user.id.startswith("01")


def test_create_user_duplicate_email():
    user_mock_repo = InMemoryUserRepo()
    crypto = Crypto()
    user_service = UserService(user_mock_repo, crypto)

    # 선행 사용자 등록
    user_service.create_user(
        email="dup@gmail.com",
        name="User1",
        password="Aa1!aaaa",
    )

    with pytest.raises(DuplicateEmailError):
        user_service.create_user(
            email="dup@gmail.com",
            name="User2",
            password="Bb2@bbbb",
        )
