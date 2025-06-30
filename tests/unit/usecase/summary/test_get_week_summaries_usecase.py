import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.summary.get_week_summaries import GetWeekSummariesUseCase
from usecase.dto.summary_dto import GetWeekSummariesRequest, GetWeekSummariesResponse

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
def get_week_summaries_usecase(mock_summary_repository, mock_week_topic_repository, mock_curriculum_repository):
    return GetWeekSummariesUseCase(
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository,
        curriculum_repository=mock_curriculum_repository
    )

@pytest.fixture
def sample_curriculum():
    """Mock Curriculum 엔티티"""
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.user_id = uuid4()
    curriculum.title = "CS 기초 과정"
    curriculum.goal = "컴퓨터 과학 기초 학습"
    curriculum.is_public = False
    return curriculum

@pytest.fixture
def public_curriculum():
    """공개 커리큘럼"""
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.user_id = uuid4()  # 다른 사용자 소유
    curriculum.title = "공개 파이썬 과정"
    curriculum.is_public = True  # 공개
    return curriculum

@pytest.fixture
def sample_week_topic(sample_curriculum):
    """Mock WeekTopic 엔티티 - sample_curriculum과 연결됨"""
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = sample_curriculum.id  # ✅ 연결
    week_topic.title = "1주차: 컴퓨터구조 기초"
    week_topic.description = "컴퓨터의 기본 구조 학습"
    week_topic.learning_goals = ["CPU 이해", "메모리 구조"]
    return week_topic

@pytest.fixture
def public_week_topic(public_curriculum):
    """공개 커리큘럼의 주차"""
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = public_curriculum.id  # ✅ 공개 커리큘럼과 연결
    week_topic.title = "1주차: 파이썬 기초"
    week_topic.description = "파이썬 기본 문법"
    week_topic.learning_goals = ["변수", "자료형"]
    return week_topic

@pytest.fixture
def sample_public_summaries(sample_week_topic):
    """해당 주차의 공개 요약들"""
    summary1 = Mock()
    summary1.id = uuid4()
    summary1.user_id = uuid4()
    summary1.week_topic_id = sample_week_topic.id  # ✅ 연결
    summary1.content = "컴퓨터구조에 대해 학습했습니다. CPU는 중앙처리장치로서..." * 3  # 긴 내용
    summary1.is_public = True
    summary1.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    summary2 = Mock()
    summary2.id = uuid4()
    summary2.user_id = uuid4()
    summary2.week_topic_id = sample_week_topic.id  # ✅ 연결
    summary2.content = "메모리 구조가 흥미로웠습니다."
    summary2.is_public = True
    summary2.created_at = datetime(2024, 1, 2, tzinfo=timezone.utc)  # 더 최신
    
    summary3 = Mock()
    summary3.id = uuid4()
    summary3.user_id = uuid4()
    summary3.week_topic_id = sample_week_topic.id  # ✅ 연결
    summary3.content = "프로세서 동작 원리를 이해할 수 있었습니다."
    summary3.is_public = True
    summary3.created_at = datetime(2024, 1, 3, tzinfo=timezone.utc)  # 가장 최신
    
    return [summary1, summary2, summary3]

class TestGetWeekSummariesUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_own_curriculum_week_summaries_successfully(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_curriculum,
        sample_week_topic,
        sample_public_summaries
    ):
        """본인 커리큘럼의 주차별 공개 요약들 조회 성공"""
        # Given
        request = GetWeekSummariesRequest(
            week_topic_id=sample_week_topic.id,
            user_id=sample_curriculum.user_id  # 본인 ID
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_summary_repository.find_by_week_topic_id_and_public = AsyncMock(return_value=sample_public_summaries)
        
        # When
        result = await get_week_summaries_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetWeekSummariesResponse)
        assert result.week_topic_title == "1주차: 컴퓨터구조 기초"
        assert result.curriculum_title == "CS 기초 과정"
        assert len(result.summaries) == 3
        
        # 최신순 정렬 확인 (summary3 → summary2 → summary1)
        assert result.summaries[0].content_preview == "프로세서 동작 원리를 이해할 수 있었습니다."
        assert result.summaries[1].content_preview == "메모리 구조가 흥미로웠습니다."
        assert result.summaries[2].content_preview.startswith("컴퓨터구조에 대해")
        assert result.summaries[2].content_preview.endswith("...")  # 150자 제한
        
        # Repository 호출 확인
        mock_week_topic_repository.find_by_id.assert_called_once_with(sample_week_topic.id)
        mock_curriculum_repository.find_by_id.assert_called_once_with(sample_curriculum.id)
        mock_summary_repository.find_by_week_topic_id_and_public.assert_called_once_with(
            sample_week_topic.id, is_public=True
        )
    
    @pytest.mark.asyncio
    async def test_execute_returns_public_curriculum_week_summaries_successfully(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        public_curriculum,
        public_week_topic
    ):
        """다른 사용자의 공개 커리큘럼 주차별 요약들 조회 성공"""
        # Given
        different_user_id = uuid4()  # 다른 사용자
        
        public_summary = Mock()
        public_summary.id = uuid4()
        public_summary.user_id = uuid4()
        public_summary.content = "파이썬 기초를 배웠습니다."
        public_summary.is_public = True
        public_summary.created_at = datetime.now(timezone.utc)
        
        request = GetWeekSummariesRequest(
            week_topic_id=public_week_topic.id,
            user_id=different_user_id
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=public_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=public_curriculum)
        mock_summary_repository.find_by_week_topic_id_and_public = AsyncMock(return_value=[public_summary])
        
        # When
        result = await get_week_summaries_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetWeekSummariesResponse)
        assert result.week_topic_title == "1주차: 파이썬 기초"
        assert result.curriculum_title == "공개 파이썬 과정"
        assert len(result.summaries) == 1
        assert result.summaries[0].content_preview == "파이썬 기초를 배웠습니다."
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_week_topic_not_found(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """존재하지 않는 주차 조회 시 에러"""
        # Given
        request = GetWeekSummariesRequest(
            week_topic_id=uuid4(),  # 존재하지 않는 ID
            user_id=uuid4()
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=None)  # 주차 없음
        
        # When & Then
        with pytest.raises(ValueError, match="주차 정보를 찾을 수 없습니다"):
            await get_week_summaries_usecase.execute(request)
        
        # 후속 Repository 호출되지 않아야 함
        mock_curriculum_repository.find_by_id.assert_not_called()
        mock_summary_repository.find_by_week_topic_id_and_public.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_curriculum_not_found(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_week_topic
    ):
        """연관된 커리큘럼이 없을 때 에러"""
        # Given
        request = GetWeekSummariesRequest(
            week_topic_id=sample_week_topic.id,
            user_id=uuid4()
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=None)  # 커리큘럼 없음
        
        # When & Then
        with pytest.raises(ValueError, match="커리큘럼 정보를 찾을 수 없습니다"):
            await get_week_summaries_usecase.execute(request)
        
        # Summary 조회는 호출되지 않아야 함
        mock_summary_repository.find_by_week_topic_id_and_public.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_access_denied(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """다른 사용자의 비공개 커리큘럼 주차 접근 시 에러"""
        # Given
        private_curriculum = Mock()
        private_curriculum.id = uuid4()
        private_curriculum.user_id = uuid4()  # 다른 사용자 소유
        private_curriculum.is_public = False  # 비공개
        
        private_week_topic = Mock()
        private_week_topic.id = uuid4()
        private_week_topic.curriculum_id = private_curriculum.id
        
        different_user_id = uuid4()  # 요청하는 사용자 (다른 사람)
        
        request = GetWeekSummariesRequest(
            week_topic_id=private_week_topic.id,
            user_id=different_user_id
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=private_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=private_curriculum)
        
        # When & Then
        with pytest.raises(ValueError, match="접근 권한이 없습니다"):
            await get_week_summaries_usecase.execute(request)
        
        # 권한 확인에서 실패하므로 Summary 조회는 호출되지 않아야 함
        mock_summary_repository.find_by_week_topic_id_and_public.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_returns_empty_when_no_public_summaries(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_curriculum,
        sample_week_topic
    ):
        """공개 요약이 없을 때 빈 리스트 반환"""
        # Given
        request = GetWeekSummariesRequest(
            week_topic_id=sample_week_topic.id,
            user_id=sample_curriculum.user_id
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_summary_repository.find_by_week_topic_id_and_public = AsyncMock(return_value=[])  # 빈 리스트
        
        # When
        result = await get_week_summaries_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetWeekSummariesResponse)
        assert result.week_topic_title == "1주차: 컴퓨터구조 기초"
        assert result.curriculum_title == "CS 기초 과정"
        assert len(result.summaries) == 0  # 빈 리스트
    
    @pytest.mark.asyncio
    async def test_execute_content_preview_truncation(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_curriculum,
        sample_week_topic
    ):
        """긴 내용이 150자로 제한되는지 확인"""
        # Given
        long_content = "A" * 200  # 200자 긴 내용
        
        long_summary = Mock()
        long_summary.id = uuid4()
        long_summary.user_id = uuid4()
        long_summary.content = long_content
        long_summary.is_public = True
        long_summary.created_at = datetime.now(timezone.utc)
        
        request = GetWeekSummariesRequest(
            week_topic_id=sample_week_topic.id,
            user_id=sample_curriculum.user_id
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_summary_repository.find_by_week_topic_id_and_public = AsyncMock(return_value=[long_summary])
        
        # When
        result = await get_week_summaries_usecase.execute(request)
        
        # Then
        assert len(result.summaries) == 1
        preview = result.summaries[0].content_preview
        assert len(preview) == 153  # 150자 + "..." (3자)
        assert preview == "A" * 150 + "..."
    
    @pytest.mark.asyncio
    async def test_execute_content_preview_no_truncation_for_short_content(
        self,
        get_week_summaries_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_curriculum,
        sample_week_topic
    ):
        """짧은 내용은 그대로 유지되는지 확인"""
        # Given
        short_content = "짧은 요약입니다."  # 150자 미만
        
        short_summary = Mock()
        short_summary.id = uuid4()
        short_summary.user_id = uuid4()
        short_summary.content = short_content
        short_summary.is_public = True
        short_summary.created_at = datetime.now(timezone.utc)
        
        request = GetWeekSummariesRequest(
            week_topic_id=sample_week_topic.id,
            user_id=sample_curriculum.user_id
        )
        
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_summary_repository.find_by_week_topic_id_and_public = AsyncMock(return_value=[short_summary])
        
        # When
        result = await get_week_summaries_usecase.execute(request)
        
        # Then
        assert len(result.summaries) == 1
        preview = result.summaries[0].content_preview
        assert preview == "짧은 요약입니다."  # "..." 없음
        assert not preview.endswith("...")