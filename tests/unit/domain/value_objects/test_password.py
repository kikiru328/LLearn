import pytest
from domain.value_objects.password import Password

def test_valid_password():
    p = Password("$2b$12$ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890")
    assert str(p).startswith("$2b$")

def test_invalid_password_format():
    with pytest.raises(ValueError):
        Password("plaintext_password")