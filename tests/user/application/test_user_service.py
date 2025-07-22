from typing import Optional
import pytest
from datetime import datetime, timezone
from user.application.auth_service import AuthService
from user.domain.entity.user import User
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.email import Email

from user.application.user_service import UserService
from user.application.exception import UserNotFoundError

from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO
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

    async def find_users(
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


async def test_get_user_sucess():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=repo, crypto=crypto)
    user_service = UserService(user_repo=repo, crypto=crypto)
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)

    # 유저 생성
    user = await auth_service.signup(
        "u@x.com",
        "Old",
        "Aa1!aaaa",
        created_at=now,
    )

    # 찾기
    assert await user_service.get_user_by_id(user.id) == user
    assert crypto.verify("Aa1!aaaa", user.password)


async def test_update_user_success():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=repo, crypto=crypto)
    user_service = UserService(user_repo=repo, crypto=crypto)

    # 먼저 유저 생성
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    u = await auth_service.signup(
        "u@x.com",
        "Old",
        "Aa1!aaaa",
        created_at=now,
    )

    # 업데이트: 이름 변경
    updated = await user_service.update_user(u.id, name="NewName")
    assert updated.name == Name("NewName")
    assert updated.updated_at > updated.created_at


async def test_update_user_not_found():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    user_service = UserService(user_repo=repo, crypto=crypto)
    with pytest.raises(UserNotFoundError):
        await user_service.update_user("nonexistent", name="XYZ")


async def test_get_users_paging():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=repo, crypto=crypto)
    user_service = UserService(user_repo=repo, crypto=crypto)

    # 25명 생성
    for i in range(25):
        await auth_service.signup(
            email=f"{i}@x.com",
            name=f"UA{i}",
            password="Aa1!aaaa",
        )

    total, page1 = await user_service.get_users(page=1, items_per_page=10)
    total2, page2 = await user_service.get_users(page=2, items_per_page=10)
    total3, page3 = await user_service.get_users(page=3, items_per_page=10)

    assert total == 25
    assert len(page1) == 10
    assert len(page2) == 10
    assert len(page3) == 5


async def test_delete_user_success():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=repo, crypto=crypto)
    user_service = UserService(user_repo=repo, crypto=crypto)

    u = await auth_service.signup(
        "del@x.com",
        "DDDD",
        "Aa1!aaaa",
    )
    await user_service.delete_user(u.id)
    # 삭제 후 조회 시 None
    assert await repo.find_by_id(u.id) is None


async def test_delete_user_not_found():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    user_service = UserService(user_repo=repo, crypto=crypto)
    with pytest.raises(UserNotFoundError):
        await user_service.delete_user("invalid-id")


async def test_change_role_sucess():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    auth_service = AuthService(user_repo=repo, crypto=crypto)
    user_service = UserService(user_repo=repo, crypto=crypto)

    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    user = await auth_service.signup(
        "u@x.com",
        "Old",
        "Aa1!aaaa",
        created_at=now,
    )

    updated_role_user = await user_service.change_role(user.id, RoleVO.ADMIN)
    assert updated_role_user.role == RoleVO.ADMIN


async def test_change_role_not_found():
    repo = InMemoryUserRepo()
    crypto = Crypto()
    user_service = UserService(user_repo=repo, crypto=crypto)

    with pytest.raises(UserNotFoundError):
        await user_service.change_role("invalid-id", RoleVO.ADMIN)
