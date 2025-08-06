import pytest
from user.domain.value_object.password import Password


@pytest.mark.parametrize(
    "raw",
    [
        "Aa1!aaaa",
        "ValidPassw0rd$",
        "Abcdef1@XyZ",
        "A1!a" * 16,
    ],
)
def test_valid_password_accept(raw):
    assert Password(raw).raw == raw


@pytest.mark.parametrize(
    "raw",
    [
        "short7$",  # 7자
        "nocapital1!",  # 대문자 없음
        "NOLOWER1!",  # 소문자 없음
        "NoNumber!",  # 숫자 없음
        "NoSpecial1",  # 특수문자 없음
        "White space1!",  # 공백 포함
        "A" * 65 + "1a!",  # 65+자
    ],
)
def test_invalid_password_rejects(raw):
    with pytest.raises(ValueError):
        Password(raw)
