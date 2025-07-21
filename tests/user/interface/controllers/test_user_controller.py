from datetime import datetime, timezone
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from fastapi.exceptions import RequestValidationError
import pytest_asyncio
from user.application.exception import DuplicateEmailError

from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.interface.exception_handler import (
    duplicate_email_handler,
    validation_exception_handler,
)
from user.interface.controllers.user_controller import (
    get_user_service,
    router as user_routers,
)


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)
    app.include_router(user_routers)
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user_success(app: FastAPI, async_client: AsyncClient):
    # -- StubUser 정의 (도메인 유저 흉내)
    class StubUser:
        id = "01TESTID1234567890"
        name = Name("tester")
        email = Email("test@example.com")
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    async def fake_create_user(name, email, password):
        return StubUser()

    stub_service = type("Svc", (), {})()
    stub_service.create_user = fake_create_user

    app.dependency_overrides[get_user_service] = (
        lambda: stub_service
    )  # no user_service, use stub_service

    response = await async_client.post(
        "/users",
        json={
            "name": "tester",
            "email": "test@example.com",
            "password": "Aa1!aaaa",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": "01TESTID1234567890",
        "name": "tester",
        "email": "test@example.com",
        "created_at": "2025-01-01T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_create_user_duplicate_email(
    app: FastAPI,
    async_client: AsyncClient,
):

    async def fake_create_user(name, email, password):
        raise DuplicateEmailError()

    stub_service = type("Svc", (), {})()
    stub_service.create_user = fake_create_user

    app.dependency_overrides[get_user_service] = lambda: stub_service

    response = await async_client.post(
        "/users",
        json={
            "name": "tester",
            "email": "test@example.com",
            "password": "Aa1!aaaa",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "이미 사용 중인 이메일입니다."}
