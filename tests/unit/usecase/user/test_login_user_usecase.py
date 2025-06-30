import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from usecase.user.login_user import LoginUserUseCase
from usecase.dto.user_dto import LoginUseCaseRequest, LoginUseCaseResponse

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"
TEST_HASHED_PASSWORD = "$2b$12$hashedpassword"


@pytest.fixture
def mock_user_repository():
    return Mock()

@pytest.fixture  
def mock_password_service():
    return Mock()

@pytest.fixture
def login_user_usecase(mock_user_repository, mock_password_service):
    return LoginUserUseCase(
        user_repository=mock_user_repository,
        password_service=mock_password_service
    )


class TestLoginUserUseCase:
    @pytest.mark.asyncio
    async def test_execute_login_successfully(self, login_user_usecase, mock_user_repository, mock_password_service):
        request = LoginUseCaseRequest(
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        
        mock_user = Mock()
        mock_user.id = uuid4()
        mock_user.email = Mock()
        mock_user.email.__str__ = Mock(return_value=TEST_EMAIL)
        mock_user.nickname = "테스트유저"
        mock_user.hashed_password = Mock()
        mock_user.hashed_password.__str__ = Mock(return_value=TEST_HASHED_PASSWORD)
        
        mock_user_repository.find_by_email = AsyncMock(return_value=mock_user)
        mock_password_service.verify_password.return_value = True

        result = await login_user_usecase.execute(request)
        
        assert isinstance(result, LoginUseCaseResponse)
        assert result.user_id == mock_user.id
        assert result.email == TEST_EMAIL
        assert result.nickname == "테스트유저"
        assert result.access_token.startswith("mock_token_")
        
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_user_not_exists(self, login_user_usecase, mock_user_repository, mock_password_service):

        request = LoginUseCaseRequest(
            email="notexist@example.com",
            password=TEST_PASSWORD
        )
        
        mock_user_repository.find_by_email = AsyncMock(return_value=None)  # 사용자 없음
        
        with pytest.raises(ValueError, match="존재하지 않는 사용자입니다"):
            await login_user_usecase.execute(request)
            
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_wrong_password(self, login_user_usecase, mock_user_repository, mock_password_service):

        request = LoginUseCaseRequest(
            email=TEST_EMAIL,
            password="wrongpassword"
        )
        

        mock_user = Mock()
        mock_user.hashed_password = Mock()
        mock_user.hashed_password.__str__ = Mock(return_value=TEST_HASHED_PASSWORD)
        
        mock_user_repository.find_by_email = AsyncMock(return_value=mock_user)
        mock_password_service.verify_password.return_value = False  # 비밀번호 틀림
        
        with pytest.raises(ValueError, match="비밀번호가 틀렸습니다"):
            await login_user_usecase.execute(request)                