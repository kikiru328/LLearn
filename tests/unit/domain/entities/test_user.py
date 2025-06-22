from uuid import uuid4
from datetime import datetime
import pytest

from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password

def test_change_nickname_success():
    """닉네임 변경 성공 테스트"""
    users = User(
        id=uuid4(),
        email=Email("test@example.com"),
        nickname="Old_Nickname",
        hashed_password=Password("$2b$12$hashedvalue..."),
        is_active=True,
        is_admin=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users.change_nickname("New_Nickname")
    assert users.nickname == "New_Nickname"

def test_change_nickname_too_short():
    """닉네임 변경 실패 테스트: 짧을 경우"""
    user = User(
        id=uuid4(),
        email=Email("test@example.com"),
        nickname="Old_Nickname",
        hashed_password=Password("$2b$12$hashedvalue..."),
        is_active=True,
        is_admin=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    with pytest.raises(ValueError, match="닉네임은 2자 이상이어야 합니다."):
        user.change_nickname("a")
