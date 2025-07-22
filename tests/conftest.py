# test/conftest.py

import sys
import os

import pytest
import pytest_asyncio

from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from httpx import AsyncClient
from httpx import ASGITransport

from DI.containers import Container
from common.auth import get_current_user
from common.auth import CurrentUser
from common.auth import Role
from user.application.exception import DuplicateEmailError
from user.interface.exception_handler import validation_exception_handler
from user.interface.exception_handler import duplicate_email_handler
from user.interface.controllers.user_controller import router as user_router

# 프로젝트 루트를 PYTHONPATH에 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# pytest-asyncio 플러그인 활성화
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def di_container() -> Container:
    container = Container()
    container.wire(modules=["user.interface.controllers.user_controller"])
    return container


@pytest.fixture
def app(di_container: Container) -> FastAPI:
    app = FastAPI()

    # 항상 같은 유저로 인증 통과
    fake_user = CurrentUser(id="01FAKEID1234567890", role=Role.USER)
    app.dependency_overrides[get_current_user] = lambda: fake_user

    # 예외 핸들러 등록
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)

    # 사용자 컨트롤러 라우터 등록
    app.include_router(user_router)
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
