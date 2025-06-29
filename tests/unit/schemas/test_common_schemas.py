import pytest
from pydantic import ValidationError
from app.schemas.common import (
    PaginationRequest,
    PaginationResponse,
    ErrorResponse,
    SuccessResponse,
    TimestampMixin,
    PublicMixin,
)
from datetime import datetime


class TestPaginationRequest:
    def test_valid_pagination_request(self):
        """정상적인 페이징 요청 테스트"""
        pagination = PaginationRequest(page=1, size=20)
        assert pagination.page == 1
        assert pagination.size == 20

    def test_default_values(self):
        """기본값 테스트"""
        pagination = PaginationRequest()
        assert pagination.page == 1
        assert pagination.size == 20

    def test_invalid_page_zero(self):
        """page가 0일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            PaginationRequest(page=0, size=20)

    def test_invalid_page_negative(self):
        """page가 음수일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            PaginationRequest(page=-1, size=20)

    def test_invalid_size_zero(self):
        """size가 0일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            PaginationRequest(page=1, size=0)

    def test_invalid_size_too_large(self):
        """size가 100 초과일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            PaginationRequest(page=1, size=101)


class TestPaginationResponse:
    def test_valid_pagination_response(self):
        """정상적인 페이징 응답 테스트"""
        response = PaginationResponse(
            total=100,
            page=1,
            size=20,
            has_next=True
        )
        assert response.total == 100
        assert response.page == 1
        assert response.size == 20
        assert response.has_next is True


class TestErrorResponse:
    def test_error_response_with_code(self):
        """에러 코드가 있는 에러 응답 테스트"""
        error = ErrorResponse(
            detail="User not found",
            error_code="USER_NOT_FOUND"
        )
        assert error.detail == "User not found"
        assert error.error_code == "USER_NOT_FOUND"

    def test_error_response_without_code(self):
        """에러 코드가 없는 에러 응답 테스트"""
        error = ErrorResponse(detail="Something went wrong")
        assert error.detail == "Something went wrong"
        assert error.error_code is None


class TestSuccessResponse:
    def test_success_response_default(self):
        """기본 성공 응답 테스트"""
        success = SuccessResponse()
        assert success.message == "Success"

    def test_success_response_custom_message(self):
        """커스텀 메시지 성공 응답 테스트"""
        success = SuccessResponse(message="User created successfully")
        assert success.message == "User created successfully"


class TestPublicMixin:
    def test_public_mixin_default(self):
        """PublicMixin 기본값 테스트"""
        mixin = PublicMixin()
        assert mixin.is_public is False

    def test_public_mixin_true(self):
        """PublicMixin True 테스트"""
        mixin = PublicMixin(is_public=True)
        assert mixin.is_public is True