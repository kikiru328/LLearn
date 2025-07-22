import pytest
from datetime import datetime, timezone
from ulid import ULID

from user.domain.repository.user_repo import IUserRepository
from user.domain.entity.user import User
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO


class InMemoryUserRepo(IUserRepository):  # 임시 Stub, Implemenation
    def __init__(self) -> None:
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

    def update(self, user: User):
        if user.id not in self._by_id:
            return None
        self._by_id[user.id] = user
        self._by_email[user.email] = user

    def find_users(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ):
        total_count: int = len(self._by_id)

        return total_count, list(self._by_id.values())

    def delete(self, id: str):
        del self._by_id[id]


def test_save_and_find():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    mock_user = User(
        id=ULID().generate(),
        email=Email("pecan@gmail.com"),
        name=Name("피칸"),
        password="hashed_dummy",
        role=RoleVO.USER,
        created_at=fake_now,
        updated_at=fake_now,
    )
    repo.save(mock_user)
    assert repo.find_by_id(mock_user.id) == mock_user
    assert repo.find_by_email(mock_user.email) == mock_user


def test_save_duplicate_raises():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    u1 = User(
        ULID().generate(),
        Email("dup@x.com"),
        Name("Test"),
        "pwd",
        RoleVO.USER,
        fake_now,
        fake_now,
    )
    u2 = User(
        ULID().generate(),
        Email("dup@x.com"),
        Name("Test1"),
        "pwd",
        RoleVO.USER,
        fake_now,
        fake_now,
    )

    repo.save(u1)
    with pytest.raises(ValueError):
        repo.save(u2)


def test_update_existing_user():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    u = User(
        ULID().generate(),
        Email("a@b.com"),
        Name("Old"),
        "pwd",
        RoleVO.USER,
        fake_now,
        fake_now,
    )
    repo.save(u)

    # 도메인 객체를 수정
    u.name = Name("New")
    repo.update(u)

    found = repo.find_by_id(u.id)
    assert found.name == Name("New")


def test_update_nonexistent_noop():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    u = User(
        ULID().generate(),
        Email("a@b.com"),
        Name("XXXX"),
        "pwd",
        RoleVO.USER,
        fake_now,
        fake_now,
    )

    # 존재하지 않는 ID 로 update
    assert repo.update(u) is None
    # 이후에도 find_by_id는 None
    assert repo.find_by_id(u.id) is None


def test_find_users_paging():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    # 15명 저장
    for i in range(15):
        u = User(
            ULID().generate(),
            Email(f"{i}@x.com"),
            Name(f"U{i}"),
            "pwd",
            RoleVO.USER,
            fake_now,
            fake_now,
        )
        repo.save(u)

    total, page1 = repo.find_users(page=1, items_per_page=10)
    assert total == 15
    assert len(page1) == 15


def test_delete_existing_user():
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    repo = InMemoryUserRepo()
    u = User(
        ULID().generate(),
        Email("del@x.com"),
        Name("DDD"),
        "pwd",
        RoleVO.USER,
        fake_now,
        fake_now,
    )
    repo.save(u)

    repo.delete(u.id)
    assert repo.find_by_id(u.id) is None


def test_delete_nonexistent_raises():
    repo = InMemoryUserRepo()
    with pytest.raises(KeyError):
        repo.delete("nonexistent-id")
