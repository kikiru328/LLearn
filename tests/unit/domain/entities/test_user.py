from uuid import uuid4
from datetime import datetime
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
    try:
        user.change_nickname("a") #short
        assert False
    except ValueError as e:
        assert "닉네임은 2자 이상이어야 합니다." in str(e)
