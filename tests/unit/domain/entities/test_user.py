from uuid import uuid4
from datetime import datetime
import pytest

from domain.entities.user import User

def test_change_nickname_success():
    users = User(
        id=uuid4(),
        email="test@example.com",
        nickname="Old_Nickname",
        hashed_password="hashed_pw",
        is_active=True,
        is_admin=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users.change_nickname("New_Nickname")
    assert users.nickname == "New_Nickname"

def test_change_nickname_too_short():
    user = User(
        id=uuid4(),
        email="test@example.com",
        nickname="Old_Nickname",
        hashed_password="hashed_pw",
        is_active=True,
        is_admin=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    with pytest.raises(ValueError) as exc_info:
        user.change_nickname("a")
    assert "닉네임은 2자 이상이어야 합니다." in str(exc_info.value)
