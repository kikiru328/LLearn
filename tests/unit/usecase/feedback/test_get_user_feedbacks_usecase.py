import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.feedback.get_user_feedbacks import GetUserFeedbacksUseCase
from usecase.dto.feedback_dto import GetUserFeedbacksRequest, GetUserFeedbacksResponse

@pytest.fixture
def mock_feedback_repository():
    return Mock()

@pytest.fixture
def mock_summary_repository():
    return Mock()

@pytest.fixture
def mock_week_topic_repository():
    return Mock()

@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture
def get_user_feedbacks_usecase(mock_feedback_repository, mock_summary_repository, mock_week_topic_repository, mock_curriculum_repository):
    return GetUserFeedbacksUseCase(
        feedback_repository=mock_feedback_repository,
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository,
        curriculum_repository=mock_curriculum_repository
    )

class TestGetUserFeedbacksUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_user_feedbacks_successfully(
        self,
        get_user_feedbacks_usecase,
        mock_feedback_repository,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """사용자 피드백 목록 조회 성공"""
        # Given
        user_id = uuid4()
        request = GetUserFeedbacksRequest(user_id=user_id)
        
        # Mock data setup
        mock_summary = Mock()
        mock_summary.id = uuid4()
        mock_summary.week_topic_id = uuid4()
        
        mock_feedback = Mock()
        mock_feedback.id = uuid4()
        mock_feedback.summary_id = mock_summary.id
        mock_feedback.content = "피드백 내용입니다"
        mock_feedback.created_at = datetime.now(timezone.utc)
        
        mock_week_topic = Mock()
        mock_week_topic.title = "1주차: 테스트"
        mock_week_topic.curriculum_id = uuid4()
        
        mock_curriculum = Mock()
        mock_curriculum.title = "테스트 커리큘럼"
        
        mock_summary_repository.find_by_user_id = AsyncMock(return_value=[mock_summary])
        mock_feedback_repository.find_by_summary_id = AsyncMock(return_value=mock_feedback)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=mock_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=mock_curriculum)
        
        # When
        result = await get_user_feedbacks_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetUserFeedbacksResponse)
        assert len(result.feedbacks) == 1
        assert result.feedbacks[0].week_topic_title == "1주차: 테스트"
        assert result.feedbacks[0].curriculum_title == "테스트 커리큘럼"