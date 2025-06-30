import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.curriculum.create_curriculum import CreateCurriculumUseCase
from usecase.dto.curriculum_dto import CreateCurriculumUseCaseRequest, CreateCurriculumUseCaseResponse, WeekTopicData


@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture
def mock_week_topic_repository():
    return Mock()

@pytest.fixture
def create_curriculum_usecase(mock_curriculum_repository, mock_week_topic_repository):
    return CreateCurriculumUseCase(
        curriculum_repository=mock_curriculum_repository,
        week_topic_repository=mock_week_topic_repository
    )

@pytest.fixture
def sample_weeks_data():
    return [
        WeekTopicData(
            week_number=1,
            title="컴퓨터 기초",
            description="컴퓨터의 기본 개념",
            learning_goals=["CPU 이해", "메모리 이해"]
        ),
        WeekTopicData(
            week_number=2,
            title="운영체제 기초",
            description="OS의 기본 개념",
            learning_goals=["프로세스 이해", "스레드 이해"]
        )
    ]


class TestCreateCurriculumUseCase:
    @pytest.mark.asyncio
    async def test_execute_creates_curriculum_successfully(
        self, 
        create_curriculum_usecase, 
        mock_curriculum_repository, 
        mock_week_topic_repository,
        sample_weeks_data
    ):

        user_id = uuid4()
        request = CreateCurriculumUseCaseRequest(
            user_id=user_id,
            title="CS 기초 학습",
            goal="컴퓨터 과학 기초 이해",
            weeks=sample_weeks_data,
            is_public=False
        )

        mock_saved_curriculum = Mock()
        mock_saved_curriculum.id = uuid4()
        mock_saved_curriculum.user_id = user_id
        mock_saved_curriculum.title = "CS 기초 학습"
        mock_saved_curriculum.goal = "컴퓨터 과학 기초 이해"
        mock_saved_curriculum.duration_weeks = 2
        mock_saved_curriculum.is_public = False
        mock_saved_curriculum.created_at = datetime.now(timezone.utc)
        mock_saved_curriculum.updated_at = datetime.now(timezone.utc)
        
        mock_curriculum_repository.save = AsyncMock(return_value=mock_saved_curriculum)

        mock_week_topics = []
        for i, week_data in enumerate(sample_weeks_data):
            mock_week = Mock()
            mock_week.week_number = week_data.week_number
            mock_week.title = week_data.title
            mock_week.description = week_data.description
            mock_week.learning_goals = week_data.learning_goals
            mock_week_topics.append(mock_week)
        
        mock_week_topic_repository.save = AsyncMock(side_effect=mock_week_topics)

        result = await create_curriculum_usecase.execute(request)

        assert isinstance(result, CreateCurriculumUseCaseResponse)
        assert result.id == mock_saved_curriculum.id
        assert result.title == "CS 기초 학습"
        assert result.duration_weeks == 2
        assert len(result.weeks) == 2

        mock_curriculum_repository.save.assert_called_once()
        assert mock_week_topic_repository.save.call_count == 2