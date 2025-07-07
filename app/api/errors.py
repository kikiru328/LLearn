"""
Global Error Handler
Domain, Usecase, Infrastructure Layer Exception--> HTTP response"""

from typing import Dict, Any, Optional
from fastapi import FastAPI
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


class ErrorResponse:

    def __init__(
        self,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ):

        self.error_code = error_code
        self.message = message
        self.details = details if details is not None else {}
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        response: Dict[str, Any] = {
            "error": {"code": self.error_code, "message": self.message}
        }
        if self.details:
            response["error"]["details"] = self.details
        return response


def map_domain_exception_to_http_error(exc: Exception) -> ErrorResponse:
    if isinstance(exc, ValueError):
        return ErrorResponse(
            error_code="VALIDATION_ERROR",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="내부 서버 오류가 발생했습니다.",
        details={"original_error": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Domain exception occurred: {exc}", exc_info=True)

    error_response = map_domain_exception_to_http_error(exc)
    return JSONResponse(
        status_code=error_response.status_code, content=error_response.to_dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")

    error_response = ErrorResponse(
        error_code="HTTP_ERROR", message=exc.detail, status_code=exc.status_code
    )
    return JSONResponse(
        status_code=error_response.status_code, content=error_response.to_dict()
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.warning(f"Validation error: {exc.errors()}")

    # Pydantic 에러를 사용자 친화적으로 변환
    error_details: Dict[str, Any] = {
        "validation_errors": exc.errors(),
        "invalid_fields": [error["loc"][-1] for error in exc.errors()],
    }

    error_response = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="요청 데이터가 올바르지 않습니다.",
        details=error_details,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    return JSONResponse(
        status_code=error_response.status_code, content=error_response.to_dict()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unexpected exception: {exc}", exc_info=True)

    error_response = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="예상치 못한 오류가 발생했습니다.",
        details={"path": str(request.url), "method": request.method},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return JSONResponse(
        status_code=error_response.status_code, content=error_response.to_dict()
    )


def register_exception_handlers(app: FastAPI) -> None:
    """FastAPI 앱에 모든 예외 핸들러 등록"""

    # 일반적인 도메인 예외들 (ValueError 등)
    app.add_exception_handler(ValueError, domain_exception_handler)

    # 모든 예외의 최종 핸들러 (catch-all)
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("예외 핸들러 등록 완료")
