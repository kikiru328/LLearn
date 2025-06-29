import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.user import (
    CreateUserRequest,
    LoginRequest,
    UpdateUserRequest,
    UserResponse,
)


class TestCreateUserRequest:
    def test_valid_create_user_request(self):
        """정상적인 회원가입 요청 테스트"""
        request = CreateUserRequest(
            email="test@example.com",
            nickname="홍길동",
            password="password123"
        )
        assert request.email == "test@example.com"
        assert request.nickname == "홍길동"
        assert request.password == "password123"

    def test_invalid_email(self):
        """잘못된 이메일 형식 테스트"""
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="잘못된이메일",
                nickname="홍길동",
                password="password123"
            )

    def test_nickname_too_short(self):
        """닉네임이 너무 짧을 때 테스트"""
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                nickname="a",  # 1자 (최소 2자)
                password="password123"
            )

    def test_nickname_too_long(self):
        """닉네임이 너무 길 때 테스트"""
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                nickname="a" * 11,  # 11자 (최대 10자)
                password="password123"
            )

    def test_password_too_short(self):
        """비밀번호가 너무 짧을 때 테스트"""
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                nickname="홍길동",
                password="1234567"  # 7자 (최소 8자)
            )


class TestLoginRequest:
    def test_valid_login_request(self):
        """정상적인 로그인 요청 테스트"""
        request = LoginRequest(
            email="test@example.com",
            password="password123"
        )
        assert request.email == "test@example.com"
        assert request.password == "password123"

    def test_invalid_email(self):
        """잘못된 이메일 형식 테스트"""
        with pytest.raises(ValidationError):
            LoginRequest(
                email="잘못된이메일",
                password="password123"
            )


class TestUpdateUserRequest:
    def test_valid_update_request(self):
        """정상적인 정보 수정 요청 테스트"""
        request = UpdateUserRequest(nickname="새닉네임")
        assert request.nickname == "새닉네임"

    def test_empty_update_request(self):
        """빈 수정 요청 테스트 (모든 필드 Optional)"""
        request = UpdateUserRequest()
        assert request.nickname is None

    def test_nickname_validation(self):
        """닉네임 검증 테스트"""
        # 너무 짧음
        with pytest.raises(ValidationError):
            UpdateUserRequest(nickname="a")
        
        # 너무 김
        with pytest.raises(ValidationError):
            UpdateUserRequest(nickname="a" * 11)


class TestUserResponse:
    def test_valid_user_response(self):
        """정상적인 사용자 응답 테스트"""
        user_id = uuid4()
        now = datetime.now()
        
        response = UserResponse(
            id=user_id,
            email="test@example.com",
            nickname="홍길동",
            is_active=True,
            is_admin=False,
            created_at=now,
            updated_at=now
        )
        
        assert response.id == user_id
        assert response.email == "test@example.com"
        assert response.nickname == "홍길동"
        assert response.is_active is True
        assert response.is_admin is False
        assert response.created_at == now
        assert response.updated_at == now

    def test_user_response_from_dict(self):
        """딕셔너리로부터 UserResponse 생성 테스트"""
        user_data = {
            "id": str(uuid4()),
            "email": "test@example.com",
            "nickname": "홍길동",
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        response = UserResponse(**user_data)
        assert response.email == "test@example.com"
        assert response.nickname == "홍길동"