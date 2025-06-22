import pytest
from domain.value_objects.email import Email

def test_valid_email():
    """
    Email 이 string으로 잘 나오는지
    Email의 domain이 잘 분리되는지 (gmail, naver)
    :return:
    """
    e = Email("test@example.com")
    assert str(e) == "test@example.com"
    assert e.domain() == "example.com"

def test_invalid_email_raises():
    """
    Email value 내 @가 없을 시 invalid
    """
    with pytest.raises(ValueError) as exc_info:
        Email("invalid-email")
    assert "유효하지 않은 이메일" in str(exc_info.value)
