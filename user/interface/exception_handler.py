from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from user.application.exception import (
    ExistEmailError,
    ExistNameError,
    UserNotFoundError,
)


async def validation_exception_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors()},
        )
    raise exc


async def value_error_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
    raise exc


async def duplicate_email_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, ExistEmailError):
        return JSONResponse(
            status_code=409,
            content={"detail": "이미 사용 중인 이메일입니다."},
        )
    raise exc


async def exist_name_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, ExistNameError):
        return JSONResponse(
            status_code=409, content={"detail": "이미 사용중인 닉네임입니다."}
        )
    raise exc


async def user_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "유저가 존재하지 않습니다."},
        )
    raise exc


def register_user_exception_handlers(app: FastAPI):
    # pydantic
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # VO
    app.add_exception_handler(ValueError, value_error_handler)
    # custom (usercase)
    app.add_exception_handler(ExistEmailError, duplicate_email_handler)
    app.add_exception_handler(ExistNameError, exist_name_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
