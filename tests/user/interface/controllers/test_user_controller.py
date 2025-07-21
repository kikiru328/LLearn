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
from user.interface.controllers.user_controller import router as user_routers
from DI.containers import Container
from dependency_injector import providers


@pytest.fixture
def di_container() -> Container:
    container = Container()
    # 컨트롤러 모듈을 명시적으로 와이어
    container.wire(modules=["user.interface.controllers.user_controller"])
    return container


@pytest.fixture
def app(di_container: Container) -> FastAPI:
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
async def test_create_user_success(
    di_container: Container,
    async_client: AsyncClient,
):
    class StubUser:
        id = "01TESTID1234567890"
        name = Name("tester")
        email = Email("test@example.com")
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    class StubService:
        async def create_user(self, name, email, password):
            return StubUser()

    di_container.user_service.override(providers.Factory(StubService))

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
    di_container: Container,
    async_client: AsyncClient,
):

    class StubService:
        async def create_user(self, name, email, password):
            raise DuplicateEmailError()

    di_container.user_service.override(providers.Factory(StubService))

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
