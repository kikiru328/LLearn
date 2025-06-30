import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.feedback.get_feedback import GetFeedbackUseCase
from usecase.dto.feedback_dto import GetFeedbackRequest, GetFeedbackResponse

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
def get_feedback_usecase(mock_feedback_repository, mock_summary_repository, mock_week_topic_repository):
    return GetFeedbackUseCase(
        feedback_repository=mock_feedback_repository,
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository
    )

class TestGetFeedbackUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_feedback_successfully(
        self,
        get_feedback_usecase,
        mock_feedback_repository,
        mock_summary_repository,
        mock_week_topic_repository
    ):
        """피드백 조회 성공"""
        # Given
        user_id = uuid4()
        summary_id = uuid4()
        
        mock_summary = Mock()
        mock_summary.id = summary_id
        mock_summary.user_id = user_id
        mock_summary.content = "테스트 요약"
        mock_summary.is_public = False
        mock_summary.week_topic_id = uuid4()
        
        mock_feedback = Mock()
        mock_feedback.id = uuid4()
        mock_feedback.summary_id = summary_id
        mock_feedback.content = "5단계 피드백 내용"
        mock_feedback.created_at = datetime.now(timezone.utc)
        
        mock_week_topic = Mock()
        mock_week_topic.title = "1주차: 테스트"
        
        request = GetFeedbackRequest(summary_id=summary_id, user_id=user_id)
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=mock_summary)
        mock_feedback_repository.find_by_summary_id = AsyncMock(return_value=mock_feedback)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=mock_week_topic)
        
        # When
        result = await get_feedback_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetFeedbackResponse)
        assert result.content == "5단계 피드백 내용"
        assert result.summary_content == "테스트 요약"
        assert result.week_topic_title == "1주차: 테스트"