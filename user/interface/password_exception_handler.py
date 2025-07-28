from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from user.application.password_exception import (
    PasswordContainsWhitespaceError,
    PasswordMissingDigitError,
    PasswordMissingLowercaseError,
    PasswordMissingSpecialCharError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)


async def password_exception_handler(request: Request, exc: Exception):
    """모든 Password 관련 예외를 처리하는 통합 핸들러"""

    if isinstance(exc, PasswordTooShortError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"비밀번호가 너무 짧습니다. {exc.length}자 입력됨, 최소 {exc.min_length}자 필요"
            },
        )

    if isinstance(exc, PasswordTooLongError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"비밀번호가 너무 깁니다. {exc.length}자 입력됨, 최대 {exc.max_length}자 허용"
            },
        )

    if isinstance(exc, PasswordMissingUppercaseError):
        return JSONResponse(
            status_code=400, content={"detail": "비밀번호에 대문자가 포함되어야 합니다"}
        )

    if isinstance(exc, PasswordMissingLowercaseError):
        return JSONResponse(
            status_code=400, content={"detail": "비밀번호에 소문자가 포함되어야 합니다"}
        )

    if isinstance(exc, PasswordMissingDigitError):
        return JSONResponse(
            status_code=400, content={"detail": "비밀번호에 숫자가 포함되어야 합니다"}
        )

    if isinstance(exc, PasswordMissingSpecialCharError):
        return JSONResponse(
            status_code=400,
            content={"detail": "비밀번호에 특수문자가 포함되어야 합니다"},
        )

    if isinstance(exc, PasswordContainsWhitespaceError):
        return JSONResponse(
            status_code=400,
            content={"detail": "비밀번호에 공백문자를 포함할 수 없습니다"},
        )

    raise exc


def register_password_exception_handlers(app: FastAPI):
    app.add_exception_handler(PasswordTooShortError, password_exception_handler)
    app.add_exception_handler(PasswordTooLongError, password_exception_handler)
    app.add_exception_handler(PasswordMissingUppercaseError, password_exception_handler)
    app.add_exception_handler(PasswordMissingLowercaseError, password_exception_handler)
    app.add_exception_handler(PasswordMissingDigitError, password_exception_handler)
    app.add_exception_handler(
        PasswordMissingSpecialCharError, password_exception_handler
    )
    app.add_exception_handler(
        PasswordContainsWhitespaceError, password_exception_handler
    )
