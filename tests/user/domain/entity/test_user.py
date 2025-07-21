import re
from ulid import ULID
from datetime import datetime, timezone
from user.domain.entity.user import User
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO


def test_user_factory_sets_defaults(mocker):
    fake_now = datetime(2025, 1, 1, tzinfo=timezone.utc)

    mock_user = User(
        id=ULID().generate(),
        email=Email("test@example.com"),  # 이미 확인
        name=Name("Alice"),  # 이미 확인
        password="hashed",
        role=RoleVO.USER,
        created_at=fake_now,
        updated_at=fake_now,
    )

    assert re.fullmatch(r"01[0-9A-Z]{24}", mock_user.id)  # ULID
    assert mock_user.created_at == fake_now
    assert mock_user.updated_at == fake_now
