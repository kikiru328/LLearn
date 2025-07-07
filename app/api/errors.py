"""
Global Error Handler
Domain, Usecase, Infrastructure Layer Exception--> HTTP response"""

from typing import Dict, Any, Optional
from fastapi import status


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
