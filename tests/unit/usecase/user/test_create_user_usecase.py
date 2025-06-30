import pytest
from unittest.mock import Mock, AsyncMock  
from uuid import uuid4
from datetime import datetime, timezone

from usecase.user.create_user import CreateUserUseCase
from usecase.dto.user_dto import CreateUserUseCaseRequest, CreateUserUseCaseResponse

TEST_PASSWORD = "password123"
TEST_HASHED_PASSWORD = "$2b$12$hashedpassword"
@pytest.fixture
def mock_user_repository():
    repository = Mock()
    repository.find_by_email = AsyncMock(return_value=None)  # AsyncMock 사용
    repository.save = AsyncMock()  # save도 AsyncMock
    return repository

@pytest.fixture  
def mock_password_service():
    return Mock()

@pytest.fixture
def create_user_usecase(mock_user_repository, mock_password_service):
    return CreateUserUseCase(
        user_repository=mock_user_repository,
        password_service=mock_password_service
    )


class TestCreateUserUseCase:
    @pytest.mark.asyncio
    async def test_execute_creates_user_successfully(self, create_user_usecase, mock_user_repository, mock_password_service):
        request = CreateUserUseCaseRequest(
            email="test@example.com",
            nickname="테스트유저",
            password=TEST_PASSWORD
        )
        
        # MOCK
        mock_user_repository.find_by_email.return_value = None # no duplicate email
        mock_password_service.hash_password.return_value = TEST_HASHED_PASSWORD
        
        mock_saved_user = Mock()
        mock_saved_user.id = uuid4()
        mock_saved_user.email = Mock()
        mock_saved_user.email.__str__ = Mock(return_value="test@example.com")
        mock_saved_user.nickname = "테스트유저"
        mock_saved_user.is_active = True
        mock_saved_user.is_admin = False
        mock_saved_user.created_at = datetime.now(timezone.utc)
        mock_saved_user.updated_at = datetime.now(timezone.utc)
        mock_user_repository.save.return_value = mock_saved_user
        
        result = await create_user_usecase.execute(request = request)
        
        assert isinstance(result, CreateUserUseCaseResponse)
        assert result.id == mock_saved_user.id
        assert result.email == "test@example.com"
        assert result.nickname == "테스트유저"
        assert result.is_active is True
        assert result.is_admin is False
        
        mock_user_repository.find_by_email.assert_called_once()
        mock_password_service.hash_password.assert_called_once_with(TEST_PASSWORD)
        mock_user_repository.save.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_email_already_exists(self, create_user_usecase, mock_user_repository, mock_password_service):
        request = CreateUserUseCaseRequest(
            email="existing@example.com",
            nickname="테스트유저",
            password=TEST_PASSWORD
        )
        
        existing_user = Mock()
        mock_user_repository.find_by_email = AsyncMock(return_value=existing_user)
        
        with pytest.raises(ValueError, match="이미 존재하는 이메일입니다."):
            await create_user_usecase.execute(request)
        
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_password_is_empty(self, create_user_usecase, mock_user_repository, mock_password_service):
        request = CreateUserUseCaseRequest(
            email="test@example.com",
            nickname="테스트유저",
            password=""
        )
        
        mock_user_repository.find_by_email = AsyncMock(return_value=None)
        mock_password_service.hash_password.side_effect = ValueError("비밀번호는 필수입니다")
        
        with pytest.raises(ValueError, match="비밀번호는 필수입니다"):
            await create_user_usecase.execute(request) 