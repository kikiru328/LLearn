import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.user.get_user_profile import GetUserProfileUseCase
from usecase.dto.user_dto import GetUserProfileRequest, GetUserProfileResponse

@pytest.fixture
def mock_user_repository():
    return Mock()

@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture
def mock_summary_repository():
    return Mock()

@pytest.fixture
def get_user_profile_usecase(mock_user_repository, mock_curriculum_repository, mock_summary_repository):
    return GetUserProfileUseCase(
        user_repository=mock_user_repository,
        curriculum_repository=mock_curriculum_repository,
        summary_repository=mock_summary_repository
    )

class TestGetUserProfileUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_user_profile_successfully(
        self,
        get_user_profile_usecase,
        mock_user_repository,
        mock_curriculum_repository,
        mock_summary_repository
    ):
        """사용자 프로필 조회 성공"""
        # Given
        user_id = uuid4()
        request = GetUserProfileRequest(user_id=user_id)
        
        mock_user = Mock()
        mock_user.id = user_id
        mock_user.email.value = "test@example.com"  # Email VO
        mock_user.nickname = "테스트유저"
        mock_user.created_at = datetime.now(timezone.utc)
        mock_user.updated_at = datetime.now(timezone.utc)
        
        mock_curriculums = [Mock(), Mock()]  # 2개
        mock_summaries = [Mock(), Mock(), Mock()]  # 3개
        
        mock_user_repository.find_by_id = AsyncMock(return_value=mock_user)
        mock_curriculum_repository.find_by_user_id = AsyncMock(return_value=mock_curriculums)
        mock_summary_repository.find_by_user_id = AsyncMock(return_value=mock_summaries)
        
        # When
        result = await get_user_profile_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetUserProfileResponse)
        assert result.email == "test@example.com"
        assert result.nickname == "테스트유저"
        assert result.curriculum_count == 2
        assert result.summary_count == 3