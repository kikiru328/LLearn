from datetime import datetime, timezone
import pytest
from ulid import ULID

from user.domain.repository.user_repo import IUserRepository
from user.domain.entity.user import User
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name


class InMemoryUserRepo(IUserRepository):  # 임시 Stub, Implemenation
    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._by_email: dict[str, User] = {}

    def save(self, user: User):
        if user.id in self._by_id or user.email in self._by_email:
            raise ValueError("duplicate user")
        self._by_id[user.id] = user
        self._by_email[user.email] = user

    def find_by_id(self, id: str):
        return self._by_id.get(id)

    def find_by_email(self, email: str):
        return self._by_email.get(email)


def test_save_and_find():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    mock_user = User(
        id=ULID().generate(),
        email=Email("pecan@gmail.com"),
        name=Name("피칸"),
        password="hashed_dummy",
        created_at=fake_now,
        updated_at=fake_now,
    )
    repo.save(mock_user)
    assert repo.find_by_id(mock_user.id) == mock_user
    assert repo.find_by_email(mock_user.email) == mock_user
