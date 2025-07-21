from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from user.application.exception import DuplicateEmailError


async def validation_exception_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(status_code=400, content=exc.errors())
    raise exc


async def duplicate_email_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, DuplicateEmailError):
        return JSONResponse(
            status_code=409,
            content={"detail": "이미 사용 중인 이메일입니다."},
        )
    raise exc
