import pytest
from datetime import datetime, timezone
from dependency_injector import providers

# from httpx import AsyncClient
from common.auth import CurrentUser, Role, get_current_user
from user.domain.value_object.name import Name
from user.domain.value_object.email import Email
from user.domain.value_object.role import RoleVO


# — GET /users/me —
@pytest.mark.asyncio
async def test_get_me_success(di_container, async_client):
    class StubUser:
        id = "01FAKEID1234567890"
        name = Name("tester")
        email = Email("test@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        updated_at = created_at

    class StubUserService:
        async def get_user_by_id(self, user_id: str):
            assert user_id == "01FAKEID1234567890"
            return StubUser()

    di_container.user_service.override(providers.Factory(StubUserService))

    resp = await async_client.get("/users/me")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": "01FAKEID1234567890",
        "name": "tester",
        "email": "test@example.com",
        "role": "USER",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


# — PUT /users/me —
@pytest.mark.asyncio
async def test_update_me_success(di_container, async_client):
    class StubUser:
        id = "01FAKEID1234567890"
        name = Name("newname")
        email = Email("test@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        updated_at = datetime(2025, 7, 24, tzinfo=timezone.utc)

    class StubUserService:
        async def update_user(self, user_id, name=None, password=None):
            assert user_id == "01FAKEID1234567890"
            assert name == "newname"
            assert password == "NewP@ssw0rd"
            return StubUser()

    di_container.user_service.override(providers.Factory(StubUserService))

    resp = await async_client.put(
        "/users/me",
        json={"name": "newname", "password": "NewP@ssw0rd"},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "id": "01FAKEID1234567890",
        "name": "newname",
        "email": "test@example.com",
        "role": "USER",
        "updated_at": "2025-07-24T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_delete_me_success(di_container, async_client):
    class StubUserService:
        async def delete_user(self, user_id: str):
            # user_id 는 conftest.py 에서 넘겨주는 fake_user.id 와 일치해야 합니다
            assert user_id == "01FAKEID1234567890"
            # 특별히 리턴값은 없으니 그냥 통과

    di_container.user_service.override(providers.Factory(StubUserService))

    resp = await async_client.delete("/users/me")
    assert resp.status_code == 204
    # body 가 비어 있어야 합니다
    assert resp.text == ""


@pytest.mark.asyncio
async def test_delete_me_unauthorized(app, async_client):
    # dependency_overrides 없애서 인증 실패 시뮬레이트
    app.dependency_overrides.clear()

    resp = await async_client.delete("/users/me")
    # 인증이 없거나 토큰 검증 실패 시 401
    assert resp.status_code == 401


# ---- Admin ----


@pytest.mark.asyncio
async def test_get_list_users_as_admin(di_container, async_client):
    # 1) 인증된 사용자를 ADMIN으로 오버라이드
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    # 2) StubUser & StubService 준비
    class StubUser:
        id = "01USER1"
        name = Name("alice")
        email = Email("alice@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        updated_at = created_at

    class StubUserService:
        async def get_users(self, page: int, items_per_page: int):
            # page, items_per_page가 정확히 전달되는지 검증
            assert page == 1
            assert items_per_page == 5
            return 1, [StubUser()]

    di_container.user_service.override(providers.Factory(StubUserService))

    # 3) 요청 & 응답 검증
    resp = await async_client.get("/users?page=1&items_per_page=5")
    assert resp.status_code == 200
    assert resp.json() == {
        "total_count": 1,
        "page": 1,
        "items_per_page": 5,
        "users": [
            {
                "id": "01USER1",
                "name": "alice",
                "email": "alice@example.com",
                "role": "USER",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
            }
        ],
    }


@pytest.mark.asyncio
async def test_get_user_by_id_as_admin(di_container, async_client):
    # — ADMIN 권한 시뮬레이션
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    # — StubUser & StubService 준비
    class StubUser:
        id = "01TARGETID"
        name = Name("bob")
        email = Email("bob@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 2, tzinfo=timezone.utc)
        updated_at = datetime(2025, 1, 3, tzinfo=timezone.utc)

    class StubUserService:
        async def get_user_by_id(self, user_id: str):
            assert user_id == "01TARGETID"
            return StubUser()

    di_container.user_service.override(providers.Factory(StubUserService))

    # — 요청 및 검증
    resp = await async_client.get("/users/01TARGETID")
    assert resp.status_code == 201
    assert resp.json() == {
        "id": "01TARGETID",
        "name": "bob",
        "email": "bob@example.com",
        "role": "USER",
        "created_at": "2025-01-02T00:00:00Z",
        "updated_at": "2025-01-03T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_get_user_by_id_forbidden(di_container, async_client):
    # — USER 권한 시뮬레이션 (관리자 아님)
    user = CurrentUser(id="01USERID", role=Role.USER)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: user

    resp = await async_client.get("/users/01TARGETID")
    # assert_admin 에 걸려서 403 Forbidden
    assert resp.status_code == 403
    assert resp.json()["detail"] == "관리자만 접근이 가능합니다."


# — PUT /users/{user_id} —
@pytest.mark.asyncio
async def test_update_user_by_admin_success(di_container, async_client):
    # ADMIN 권한
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    # StubUserService
    class StubUser:
        id = "01TARGETID"
        name = Name("updated")
        email = Email("upd@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        updated_at = datetime(2025, 8, 1, tzinfo=timezone.utc)

    class StubService:
        async def update_user(self, user_id, name=None, password=None):
            assert user_id == "01TARGETID"
            assert name == "updated"
            assert password == "NewP@ssw0rd2"
            return StubUser()

    di_container.user_service.override(providers.Factory(StubService))

    resp = await async_client.put(
        "/users/01TARGETID",
        json={"name": "updated", "password": "NewP@ssw0rd2"},
    )
    assert resp.status_code == 201
    assert resp.json() == {
        "id": "01TARGETID",
        "name": "updated",
        "email": "upd@example.com",
        "role": "USER",
        # "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-08-01T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_update_user_by_admin_forbidden(di_container, async_client):
    # USER 권한
    user = CurrentUser(id="01USERID", role=Role.USER)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: user

    resp = await async_client.put(
        "/users/01TARGETID",
        json={"name": "x", "password": "p"},
    )
    assert resp.status_code == 403
    assert resp.json()["detail"] == "관리자만 접근이 가능합니다."


# — DELETE /users/{user_id} —
@pytest.mark.asyncio
async def test_delete_user_by_admin_success(di_container, async_client):
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    class StubService:
        async def delete_user(self, user_id):
            assert user_id == "01TARGETID"

    di_container.user_service.override(providers.Factory(StubService))

    resp = await async_client.delete("/users/01TARGETID")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_by_admin_forbidden(di_container, async_client):
    user = CurrentUser(id="01USERID", role=Role.USER)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: user

    resp = await async_client.delete("/users/01TARGETID")
    assert resp.status_code == 403
    assert resp.json()["detail"] == "관리자만 접근이 가능합니다."


@pytest.mark.asyncio
async def test_change_role_sucess(di_container, async_client):

    # admin 권한
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    class StubUser:
        id = "01TARGETID"
        name = Name("Bob")
        email = Email("bob@example.com")
        role = RoleVO.ADMIN
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        updated_at = datetime(2025, 1, 10, tzinfo=timezone.utc)

    class StubService:
        async def change_role(self, user_id: str, role=RoleVO):
            assert user_id == "01TARGETID"
            assert role == RoleVO.ADMIN
            return StubUser()

    di_container.user_service.override(providers.Factory(StubService))

    response = await async_client.patch(
        "/users/01TARGETID/role",
        json={"role": "ADMIN"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "01TARGETID",
        "name": "Bob",
        "email": "bob@example.com",
        "role": "ADMIN",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-10T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_change_role_invalid_value(di_container, async_client):
    # ADMIN 권한 유지
    admin = CurrentUser(id="01ADMINID", role=Role.ADMIN)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: admin

    # 잘못된 role 값 → Pydantic 검증 실패 → 422
    resp = await async_client.patch(
        "/users/01TARGETID/role",
        json={"role": "SUPERADMIN"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_change_role_forbidden(di_container, async_client):
    # USER 권한 시뮬레이션
    user = CurrentUser(id="01USERID", role=Role.USER)
    async_client._transport.app.dependency_overrides[get_current_user] = lambda: user

    resp = await async_client.patch(
        "/users/01TARGETID/role",
        json={"role": "ADMIN"},
    )
    assert resp.status_code == 403
    assert resp.json()["detail"] == "관리자만 접근이 가능합니다."
