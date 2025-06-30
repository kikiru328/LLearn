import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.curriculum.get_user_curriculums import GetUserCurriculumsUseCase
from usecase.dto.curriculum_dto import GetUserCurriculumsRequest, GetUserCurriculumsResponse, CurriculumSummaryData

@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture
def get_user_curriculums_usecase(mock_curriculum_repository):
    return GetUserCurriculumsUseCase(curriculum_repository=mock_curriculum_repository)

@pytest.fixture
def sample_curriculums():
    """Mock Curriculum 엔티티들"""
    mock_curriculum1 = Mock()
    mock_curriculum1.id = uuid4()
    mock_curriculum1.title = "CS 기초 과정"
    mock_curriculum1.goal = "컴퓨터 과학 기초 이해"
    mock_curriculum1.duration_weeks = 12
    mock_curriculum1.is_public = False
    mock_curriculum1.created_at = datetime.now(timezone.utc)
    mock_curriculum1.updated_at = datetime.now(timezone.utc)
    
    mock_curriculum2 = Mock()
    mock_curriculum2.id = uuid4()
    mock_curriculum2.title = "파이썬 마스터"
    mock_curriculum2.goal = "파이썬 완전 정복"
    mock_curriculum2.duration_weeks = 8
    mock_curriculum2.is_public = True
    mock_curriculum2.created_at = datetime.now(timezone.utc)
    mock_curriculum2.updated_at = datetime.now(timezone.utc)
    
    return [mock_curriculum1, mock_curriculum2]

class TestGetUserCurriculumsUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_user_curriculums_successfully(
        self,
        get_user_curriculums_usecase,
        mock_curriculum_repository,
        sample_curriculums
    ):
        # Given
        user_id = uuid4()
        request = GetUserCurriculumsRequest(user_id=user_id)
        mock_curriculum_repository.find_by_user_id = AsyncMock(return_value=sample_curriculums)
        
        # When
        result = await get_user_curriculums_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetUserCurriculumsResponse)
        assert len(result.curriculums) == 2
        assert result.curriculums[0].title == "CS 기초 과정"
        assert result.curriculums[1].title == "파이썬 마스터"
        
        mock_curriculum_repository.find_by_user_id.assert_called_once_with(user_id)