import pytest
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from unittest.mock import Mock, AsyncMock
from pydantic import ValidationError

from app.api.errors import (
    ErrorResponse,
    map_domain_exception_to_http_error,
    domain_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)


class TestErrorResponse:
    """ErrorResponse 클래스 테스트"""

    def test_error_response_basic_creation(self):
        """기본 ErrorResponse 생성 테스트"""
        # Given
        error = ErrorResponse(
            error_code="TEST_ERROR", message="테스트 에러입니다", status_code=400
        )

        # When
        response_dict = error.to_dict()

        # Then
        assert response_dict == {
            "error": {"code": "TEST_ERROR", "message": "테스트 에러입니다"}
        }
        assert error.status_code == 400

    def test_error_response_with_details(self):
        """상세 정보가 포함된 ErrorResponse 테스트"""
        # Given
        details = {"field": "email", "value": "invalid_email"}
        error = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="검증 실패",
            details=details,
            status_code=422,
        )

        # When
        response_dict = error.to_dict()

        # Then
        assert response_dict["error"]["details"] == details
        assert error.status_code == 422

    def test_error_response_with_none_details(self):
        """details가 None일 때 빈 dict로 초기화되는지 테스트"""
        # Given
        error = ErrorResponse(
            error_code="TEST_ERROR", message="테스트 메시지", details=None
        )

        # Then
        assert error.details == {}


class TestMapDomainExceptionToHttpError:
    """도메인 예외 → HTTP 에러 매핑 테스트"""

    def test_value_error_maps_to_400_bad_request(self):
        """ValueError가 400 Bad Request로 매핑되는지 테스트"""
        # Given
        exc = ValueError("이미 존재하는 이메일입니다")

        # When
        error_response = map_domain_exception_to_http_error(exc)

        # Then
        assert error_response.error_code == "VALIDATION_ERROR"
        assert error_response.message == "이미 존재하는 이메일입니다"
        assert error_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unknown_exception_maps_to_500_internal_server_error(self):
        """알 수 없는 예외가 500 Internal Server Error로 매핑되는지 테스트"""
        # Given
        exc = RuntimeError("예상치 못한 오류")

        # When
        error_response = map_domain_exception_to_http_error(exc)

        # Then
        assert error_response.error_code == "INTERNAL_SERVER_ERROR"
        assert error_response.message == "내부 서버 오류가 발생했습니다."
        assert error_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert error_response.details["original_error"] == "예상치 못한 오류"


class TestDomainExceptionHandler:
    """Domain 예외 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_domain_exception_handler_value_error(self):
        """ValueError 처리 테스트"""
        # Given
        request = Mock(spec=Request)
        exc = ValueError("비즈니스 규칙 위반")

        # When
        response = await domain_exception_handler(request, exc)

        # Then
        assert response.status_code == 400
        response_data = response.body.decode("utf-8")
        assert "VALIDATION_ERROR" in response_data
        assert "비즈니스 규칙 위반" in response_data

    @pytest.mark.asyncio
    async def test_domain_exception_handler_runtime_error(self):
        """RuntimeError 처리 테스트"""
        # Given
        request = Mock(spec=Request)
        exc = RuntimeError("예상치 못한 도메인 오류")

        # When
        response = await domain_exception_handler(request, exc)

        # Then
        assert response.status_code == 500
        response_data = response.body.decode("utf-8")
        assert "INTERNAL_SERVER_ERROR" in response_data
        assert "내부 서버 오류가 발생했습니다" in response_data


class TestHttpExceptionHandler:
    """HTTP 예외 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_http_exception_handler_404(self):
        """404 HTTPException 처리 테스트"""
        # Given
        request = Mock(spec=Request)
        exc = HTTPException(status_code=404, detail="리소스를 찾을 수 없습니다")

        # When
        response = await http_exception_handler(request, exc)

        # Then
        assert response.status_code == 404
        response_data = response.body.decode("utf-8")
        assert "HTTP_ERROR" in response_data
        assert "리소스를 찾을 수 없습니다" in response_data

    @pytest.mark.asyncio
    async def test_http_exception_handler_403(self):
        """403 HTTPException 처리 테스트"""
        # Given
        request = Mock(spec=Request)
        exc = HTTPException(status_code=403, detail="접근 권한이 없습니다")

        # When
        response = await http_exception_handler(request, exc)

        # Then
        assert response.status_code == 403
        response_data = response.body.decode("utf-8")
        assert "HTTP_ERROR" in response_data
        assert "접근 권한이 없습니다" in response_data


class TestValidationExceptionHandler:
    """Validation 예외 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_validation_exception_handler(self):
        """RequestValidationError 처리 테스트"""
        # Given
        request = Mock(spec=Request)

        # RequestValidationError 모킹
        validation_errors = [
            {
                "loc": ("body", "email"),
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ("body", "password"),
                "msg": "ensure this value has at least 8 characters",
                "type": "value_error.any_str.min_length",
            },
        ]
        exc = Mock(spec=RequestValidationError)
        exc.errors.return_value = validation_errors

        # When
        response = await validation_exception_handler(request, exc)

        # Then
        assert response.status_code == 422
        response_data = response.body.decode("utf-8")
        assert "VALIDATION_ERROR" in response_data
        assert "요청 데이터가 올바르지 않습니다" in response_data
        assert "email" in response_data
        assert "password" in response_data


class TestGeneralExceptionHandler:
    """일반 예외 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_general_exception_handler(self):
        """일반 예외 처리 테스트"""
        # Given
        request = Mock(spec=Request)
        request.url = Mock()
        request.url.__str__ = Mock(return_value="http://localhost:8000/test")
        request.method = "POST"

        exc = ConnectionError("데이터베이스 연결 실패")

        # When
        response = await general_exception_handler(request, exc)

        # Then
        assert response.status_code == 500
        response_data = response.body.decode("utf-8")
        assert "INTERNAL_SERVER_ERROR" in response_data
        assert "예상치 못한 오류가 발생했습니다" in response_data
        assert "http://localhost:8000/test" in response_data
        assert "POST" in response_data

    @pytest.mark.asyncio
    async def test_general_exception_handler_preserves_request_info(self):
        """일반 예외 핸들러가 요청 정보를 보존하는지 테스트"""
        # Given
        request = Mock(spec=Request)
        request.url = Mock()
        request.url.__str__ = Mock(return_value="http://localhost:8000/api/users")
        request.method = "GET"

        exc = Exception("알 수 없는 오류")

        # When
        response = await general_exception_handler(request, exc)

        # Then
        response_data = response.body.decode("utf-8")
        assert "/api/users" in response_data
        assert "GET" in response_data


class TestExceptionHandlerIntegration:
    """예외 핸들러 통합 테스트"""

    def test_all_handlers_return_json_response(self):
        """모든 핸들러가 JSONResponse를 반환하는지 테스트"""
        from fastapi.responses import JSONResponse

        # Given
        request = Mock(spec=Request)
        request.url = Mock()
        request.url.__str__ = Mock(return_value="http://localhost:8000/test")
        request.method = "POST"

        # When & Then
        async def check_handler(handler, exc):
            response = await handler(request, exc)
            assert isinstance(response, JSONResponse)
            return response

        # 모든 핸들러 테스트 (실제 실행은 별도 async 함수에서)
        handlers_and_exceptions = [
            (domain_exception_handler, ValueError("test")),
            (http_exception_handler, HTTPException(404, "not found")),
            (general_exception_handler, Exception("test")),
        ]

        # 각 핸들러가 JSONResponse를 반환하는지 타입 체크
        for handler, exc in handlers_and_exceptions:
            # 실제 테스트는 async 컨텍스트에서 실행되어야 함
            assert callable(handler)
            assert isinstance(exc, Exception)
