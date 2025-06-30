import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.feedback.generate_feedback import GenerateFeedbackUseCase
from usecase.dto.feedback_dto import GenerateFeedbackUseCaseRequest, GenerateFeedbackUseCaseResponse


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
def mock_llm_service():
    return Mock()

@pytest.fixture
def generate_feedback_usecase(
    mock_feedback_repository, 
    mock_summary_repository, 
    mock_week_topic_repository, 
    mock_llm_service
):
    return GenerateFeedbackUseCase(
        feedback_repository=mock_feedback_repository,
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository,
        llm_service=mock_llm_service
    )


class TestGenerateFeedbackUseCase:
    @pytest.mark.asyncio
    async def test_execute_generates_feedback_successfully(
        self, 
        generate_feedback_usecase,
        mock_feedback_repository,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_llm_service
    ):
        summary_id = uuid4()
        week_topic_id = uuid4()
        
        request = GenerateFeedbackUseCaseRequest(summary_id=summary_id)
        
        mock_summary = Mock()
        mock_summary.week_topic_id = week_topic_id
        mock_summary.content = "프로세스는 독립적인 메모리 공간을 가집니다..."
        mock_summary_repository.find_by_id = AsyncMock(return_value=mock_summary)
  
        mock_week_topic = Mock()
        mock_week_topic.title = "운영체제 기초"
        mock_week_topic.description = "프로세스와 스레드의 개념을 학습"
        mock_week_topic.learning_goals = ["프로세스 이해", "스레드 이해"]
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=mock_week_topic)
        
        mock_feedback_content = """
        1. ✅ 정확성 확인: 프로세스의 독립성에 대해 올바르게 이해하셨습니다
        2. 📝 누락 보충: 스레드와의 차이점에 대해 설명해드리겠습니다...
        3. ⚠️ 오류 수정: 특별한 오류는 없습니다
        4. 🤔 심화 질문: 컨텍스트 스위칭에 대해 설명해보세요
        5. 📚 확장 학습: 다음은 IPC에 대해 학습해보세요
        """
        mock_llm_service.generate_feedback = AsyncMock(return_value=mock_feedback_content)

        mock_saved_feedback = Mock()
        mock_saved_feedback.id = uuid4()
        mock_saved_feedback.summary_id = summary_id
        mock_saved_feedback.content = mock_feedback_content
        mock_saved_feedback.created_at = datetime.now(timezone.utc)
        mock_feedback_repository.save = AsyncMock(return_value=mock_saved_feedback)

        result = await generate_feedback_usecase.execute(request)
        
        assert isinstance(result, GenerateFeedbackUseCaseResponse)
        assert result.id == mock_saved_feedback.id
        assert result.summary_id == summary_id
        assert "정확성 확인" in result.content

        mock_summary_repository.find_by_id.assert_called_once_with(summary_id)
        mock_week_topic_repository.find_by_id.assert_called_once_with(week_topic_id)
        mock_llm_service.generate_feedback.assert_called_once_with(
            summary_content="프로세스는 독립적인 메모리 공간을 가집니다...",
            week_topic_title="운영체제 기초",
            week_topic_description="프로세스와 스레드의 개념을 학습",
            learning_goals=["프로세스 이해", "스레드 이해"]
        )
        mock_feedback_repository.save.assert_called_once()