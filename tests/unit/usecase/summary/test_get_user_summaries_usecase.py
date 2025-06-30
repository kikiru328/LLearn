import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.summary.get_user_summaries import GetUserSummariesUseCase
from usecase.dto.summary_dto import GetUserSummariesRequest, GetUserSummariesResponse

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
def get_user_summaries_usecase(mock_summary_repository, mock_week_topic_repository, mock_curriculum_repository):
    return GetUserSummariesUseCase(
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository,
        curriculum_repository=mock_curriculum_repository
    )

@pytest.fixture
def sample_curriculum():
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.title = "CS 기초 과정"
    return curriculum

@pytest.fixture
def sample_week_topic(sample_curriculum):
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = sample_curriculum.id  # 
    week_topic.title = "1주차: 컴퓨터구조 기초"
    return week_topic

@pytest.fixture
def sample_summaries(sample_week_topic):
    summary1 = Mock()
    summary1.id = uuid4()
    summary1.week_topic_id = sample_week_topic.id  # 
    summary1.content = "컴퓨터구조에 대해 학습했습니다. CPU는 중앙처리장치로서..." * 5  # 긴 내용
    summary1.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    summary1.updated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    summary2 = Mock()
    summary2.id = uuid4()
    summary2.week_topic_id = sample_week_topic.id  # 
    summary2.content = "짧은 요약입니다."
    summary2.created_at = datetime(2024, 1, 2, tzinfo=timezone.utc)  # 더 최신
    summary2.updated_at = datetime(2024, 1, 2, tzinfo=timezone.utc)
    
    return [summary1, summary2]

class TestGetUserSummariesUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_user_summaries_successfully(
        self,
        get_user_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_curriculum,
        sample_week_topic,
        sample_summaries
    ):
        """사용자 요약 목록 조회 성공"""
        # Given
        user_id = uuid4()
        request = GetUserSummariesRequest(user_id=user_id)
        
        mock_summary_repository.find_by_user_id = AsyncMock(return_value=sample_summaries)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        
        # When
        result = await get_user_summaries_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetUserSummariesResponse)
        assert len(result.summaries) == 2
        
        # 최신순 정렬 확인 (summary2가 먼저)
        assert result.summaries[0].content_preview == "짧은 요약입니다."
        assert result.summaries[1].content_preview.startswith("컴퓨터구조에 대해")
        assert result.summaries[1].content_preview.endswith("...")  # 100자 제한
        
        # 연관 정보 확인
        assert result.summaries[0].week_topic_title == "1주차: 컴퓨터구조 기초"
        assert result.summaries[0].curriculum_title == "CS 기초 과정"
    
    @pytest.mark.asyncio
    async def test_execute_skips_summary_when_week_topic_not_found(
        self,
        get_user_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_summaries
    ):
        """주차 정보가 없는 요약은 스킵"""
        # Given
        user_id = uuid4()
        request = GetUserSummariesRequest(user_id=user_id)
        
        mock_summary_repository.find_by_user_id = AsyncMock(return_value=sample_summaries)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=None)  # 주차 없음
        
        # When
        result = await get_user_summaries_usecase.execute(request)
        
        # Then
        assert len(result.summaries) == 0  # 모두 스킵됨
    
    @pytest.mark.asyncio
    async def test_execute_returns_empty_list_when_no_summaries(
        self,
        get_user_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """요약이 없을 때 빈 리스트 반환"""
        # Given
        user_id = uuid4()
        request = GetUserSummariesRequest(user_id=user_id)
        
        mock_summary_repository.find_by_user_id = AsyncMock(return_value=[])  # 빈 리스트
        
        # When
        result = await get_user_summaries_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetUserSummariesResponse)
        assert len(result.summaries) == 0