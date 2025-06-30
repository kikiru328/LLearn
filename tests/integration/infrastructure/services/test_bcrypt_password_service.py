import bcrypt
from pydantic import ValidationError
import pytest

from infrastructure.services.bcrypt_password_service import BcryptPasswordService


TEST_PASSWORD = "testpassword"
WRONG_PASSWORD = "wrongpassword"

@pytest.fixture
def password_service():
    return BcryptPasswordService()

class TestBcryptPasswordService:
    def test_hash_password_returns_different_hash_each_time(self, password_service):
        password = TEST_PASSWORD
        
        hashed_pwd = password_service.hash_password(password)
        
        assert isinstance(hashed_pwd, str)
        assert len(hashed_pwd) > 0
        
    def test_verify_password_with_correct_password_returns_true(self, password_service):
        password = TEST_PASSWORD
        hashed_pwd = password_service.hash_password(password)
        
        result = password_service.verify_password(password, hashed_pwd)
        
        assert result is True
        
    def test_verify_password_with_wrong_password_returns_false(self, password_service):
        correct_password = TEST_PASSWORD
        wrong_password = WRONG_PASSWORD
        hashed_pwd = password_service.hash_password(correct_password)
        result = password_service.verify_password(wrong_password, hashed_pwd)
    
        assert result is False
        
    def test_hash_password_with_empty_string(self, password_service):
        empty_password = ""
        with pytest.raises(ValueError, match="비밀번호는 필수입니다"):
            password_service.hash_password(empty_password)