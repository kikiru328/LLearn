import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.summary.create_summary import CreateSummaryUseCase
from usecase.dto.summary_dto import CreateSummaryUseCaseRequest, CreateSummaryUseCaseResponse


@pytest.fixture
def mock_summary_repository():
    return Mock()

@pytest.fixture
def mock_week_topic_repository():
    return Mock()

@pytest.fixture
def create_summary_usecase(mock_summary_repository, mock_week_topic_repository):
    return CreateSummaryUseCase(
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository
    )


class TestCreateSummaryUseCase:
    @pytest.mark.asyncio
    async def test_execute_creates_summary_successfully(
        self, 
        create_summary_usecase, 
        mock_summary_repository, 
        mock_week_topic_repository
    ):

        user_id = uuid4()
        week_topic_id = uuid4()
        request = CreateSummaryUseCaseRequest(
            user_id=user_id,
            week_topic_id=week_topic_id,
            content="이번 주차에서 배운 내용은...",
            is_public=True
        )
        

        mock_week_topic = Mock()  # WeekTopic 존재
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=mock_week_topic)
        
        mock_saved_summary = Mock()
        mock_saved_summary.id = uuid4()
        mock_saved_summary.user_id = user_id
        mock_saved_summary.week_topic_id = week_topic_id
        mock_saved_summary.content = "이번 주차에서 배운 내용은..."
        mock_saved_summary.is_public = True
        mock_saved_summary.created_at = datetime.now(timezone.utc)
        mock_saved_summary.updated_at = datetime.now(timezone.utc)
        
        mock_summary_repository.save = AsyncMock(return_value=mock_saved_summary)
        

        result = await create_summary_usecase.execute(request)
        

        assert isinstance(result, CreateSummaryUseCaseResponse)
        assert result.id == mock_saved_summary.id
        assert result.user_id == user_id
        assert result.week_topic_id == week_topic_id
        assert result.content == "이번 주차에서 배운 내용은..."
        assert result.is_public is True
        

        mock_week_topic_repository.find_by_id.assert_called_once_with(week_topic_id)
        mock_summary_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_week_topic_not_exists(
        self, 
        create_summary_usecase, 
        mock_summary_repository, 
        mock_week_topic_repository
    ):

        request = CreateSummaryUseCaseRequest(
            user_id=uuid4(),
            week_topic_id=uuid4(),
            content="내용",
            is_public=False
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=None)  # WeekTopic 없음
        
        with pytest.raises(ValueError, match="존재하지 않는 주차 주제입니다"):
            await create_summary_usecase.execute(request)