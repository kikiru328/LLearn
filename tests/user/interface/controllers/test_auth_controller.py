from datetime import datetime, timezone
import pytest
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from fastapi.exceptions import RequestValidationError
import pytest_asyncio
from user.application.exception import DuplicateEmailError

from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO
from user.interface.exception_handler import (
    duplicate_email_handler,
    validation_exception_handler,
)
from user.interface.controllers.auth_controller import router as auth_routers
from user.interface.controllers.user_controller import router as user_routers
from DI.containers import Container
from dependency_injector import providers


@pytest.fixture
def di_container() -> Container:
    container = Container()
    # 컨트롤러 모듈을 명시적으로 와이어
    container.wire(
        modules=[
            "user.interface.controllers.user_controller",
            "user.interface.controllers.auth_controller",
        ]
    )
    return container


@pytest.fixture
def app(di_container: Container) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)
    app.include_router(user_routers)
    app.include_router(auth_routers)
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_sign_up_sucess(
    di_container: Container,
    async_client: AsyncClient,
):
    class StubUser:
        id = "01TESTID1234567890"
        name = Name("tester")
        email = Email("test@example.com")
        role = RoleVO.USER
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    class StubAuthService:
        async def signup(self, name, email, password):
            return StubUser()

    di_container.auth_service.override(providers.Factory(StubAuthService))

    response = await async_client.post(
        "/auth/signup",
        json={
            "name": "test",
            "email": "test@example.com",
            "password": "Aa1!aaaa",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "01TESTID1234567890",
        "name": "tester",
        "email": "test@example.com",
        "role": "USER",
        "created_at": "2025-01-01T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_signup_missing_field(async_client: AsyncClient):
    # name 누락
    response = await async_client.post(
        "/auth/signup",
        json={"email": "a@b.com", "password": "Aa1!aaaa"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_signup_invalid_email(async_client: AsyncClient):
    # 이메일 포맷 오류
    response = await async_client.post(
        "/auth/signup",
        json={"name": "tester", "email": "not-an-email", "password": "Aa1!aaaa"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_signup_duplicate_email(
    di_container: Container,
    async_client: AsyncClient,
):
    # 중복 이메일 시 서비스에서 오류 발생하도록 Stub 설정
    class StubAuthService:
        async def signup(self, name, email, password):
            raise DuplicateEmailError("이미 사용 중인 이메일입니다.")

    di_container.auth_service.override(providers.Factory(StubAuthService))

    response = await async_client.post(
        "/auth/signup",
        json={"name": "tester", "email": "dup@test.com", "password": "Aa1!aaaa"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "이미 사용 중인 이메일입니다."


@pytest.mark.asyncio
async def test_login_success(
    di_container: Container,
    async_client: AsyncClient,
):

    class StubAuthService:
        async def login(self, email, password):
            return "fake-jwt-token", RoleVO.USER

    di_container.auth_service.override(providers.Factory(StubAuthService))

    response = await async_client.post(
        "/auth/login",
        data={
            "username": "user@example.com",
            "password": "Aa1!aaaa",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "fake-jwt-token",
        "token_type": "bearer",
        "role": "USER",
    }


@pytest.mark.asyncio
async def test_login_missing_field(async_client: AsyncClient):
    # 폼 필드 누락 → 400 Bad Request
    response = await async_client.post(
        "/auth/login",
        data={"username": "user@example.com"},  # password 누락
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_invalid_credentials(
    di_container: Container, async_client: AsyncClient
):
    # StubAuthService.login 이 HTTPException(401) 을 던지도록 오버라이드
    class StubAuthService:
        async def login(self, email, password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    di_container.auth_service.override(providers.Factory(StubAuthService))

    response = await async_client.post(
        "/auth/login",
        data={"username": "noone@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
