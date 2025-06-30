import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.summary.get_summary_detail import GetSummaryDetailUseCase
from usecase.dto.summary_dto import GetSummaryDetailRequest, GetSummaryDetailResponse

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
def get_summary_detail_usecase(mock_summary_repository, mock_week_topic_repository, mock_curriculum_repository):
    return GetSummaryDetailUseCase(
        summary_repository=mock_summary_repository,
        week_topic_repository=mock_week_topic_repository,
        curriculum_repository=mock_curriculum_repository
    )

@pytest.fixture
def sample_curriculum():
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.title = "CS 기초 과정"
    curriculum.goal = "컴퓨터 과학 기초를 체계적으로 학습하기"
    return curriculum

@pytest.fixture
def sample_week_topic(sample_curriculum):
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = sample_curriculum.id  # ✅ 연결
    week_topic.title = "1주차: 컴퓨터구조 기초"
    week_topic.description = "컴퓨터의 기본 구조를 학습합니다"
    week_topic.learning_goals = ["CPU 이해", "메모리 구조", "폰노이만 구조"]
    return week_topic

@pytest.fixture
def sample_summary(sample_week_topic):
    summary = Mock()
    summary.id = uuid4()
    summary.user_id = uuid4()
    summary.week_topic_id = sample_week_topic.id  # ✅ 연결
    summary.content = "컴퓨터구조에 대해 학습했습니다. CPU는 중앙처리장치로서 프로그램의 명령어를 해석하고 실행하는 역할을 담당합니다..."
    summary.is_public = False
    summary.created_at = datetime.now(timezone.utc)
    summary.updated_at = datetime.now(timezone.utc)
    return summary

@pytest.fixture
def public_summary(sample_week_topic):
    summary = Mock()
    summary.id = uuid4()
    summary.user_id = uuid4()  # 다른 사용자 소유
    summary.week_topic_id = sample_week_topic.id
    summary.content = "공개된 학습 요약입니다."
    summary.is_public = True  # 공개
    summary.created_at = datetime.now(timezone.utc)
    summary.updated_at = datetime.now(timezone.utc)
    return summary

class TestGetSummaryDetailUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_own_summary_successfully(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_summary,
        sample_week_topic,
        sample_curriculum
    ):
        """본인 요약 상세 조회 성공"""
        # Given
        request = GetSummaryDetailRequest(
            summary_id=sample_summary.id,
            user_id=sample_summary.user_id  # 본인 ID
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=sample_summary)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        
        # When
        result = await get_summary_detail_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetSummaryDetailResponse)
        assert result.id == sample_summary.id
        assert result.user_id == sample_summary.user_id
        assert result.content == sample_summary.content  # 전체 내용
        assert result.is_public == False
        
        # 연관 정보 확인
        assert result.week_topic_title == "1주차: 컴퓨터구조 기초"
        assert result.week_topic_description == "컴퓨터의 기본 구조를 학습합니다"
        assert result.learning_goals == ["CPU 이해", "메모리 구조", "폰노이만 구조"]
        assert result.curriculum_title == "CS 기초 과정"
        assert result.curriculum_goal == "컴퓨터 과학 기초를 체계적으로 학습하기"
        
        # Repository 호출 확인
        mock_summary_repository.find_by_id.assert_called_once_with(sample_summary.id)
        mock_week_topic_repository.find_by_id.assert_called_once_with(sample_week_topic.id)
        mock_curriculum_repository.find_by_id.assert_called_once_with(sample_curriculum.id)
    
    @pytest.mark.asyncio
    async def test_execute_returns_public_summary_successfully(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        public_summary,
        sample_week_topic,
        sample_curriculum
    ):
        """다른 사용자의 공개 요약 조회 성공"""
        # Given
        different_user_id = uuid4()  # 다른 사용자
        request = GetSummaryDetailRequest(
            summary_id=public_summary.id,
            user_id=different_user_id
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=public_summary)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        
        # When
        result = await get_summary_detail_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetSummaryDetailResponse)
        assert result.content == "공개된 학습 요약입니다."
        assert result.is_public == True
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_summary_not_found(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """존재하지 않는 요약 조회 시 에러"""
        # Given
        request = GetSummaryDetailRequest(
            summary_id=uuid4(),  # 존재하지 않는 ID
            user_id=uuid4()
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=None)  # 요약 없음
        
        # When & Then
        with pytest.raises(ValueError, match="요약을 찾을 수 없습니다"):
            await get_summary_detail_usecase.execute(request)
        
        # 후속 Repository 호출되지 않아야 함
        mock_week_topic_repository.find_by_id.assert_not_called()
        mock_curriculum_repository.find_by_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_access_denied(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository
    ):
        """다른 사용자의 비공개 요약 접근 시 에러"""
        # Given
        private_summary = Mock()
        private_summary.id = uuid4()
        private_summary.user_id = uuid4()  # 다른 사용자 소유
        private_summary.is_public = False  # 비공개
        
        different_user_id = uuid4()  # 요청하는 사용자 (다른 사람)
        
        request = GetSummaryDetailRequest(
            summary_id=private_summary.id,
            user_id=different_user_id
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=private_summary)
        
        # When & Then
        with pytest.raises(ValueError, match="접근 권한이 없습니다"):
            await get_summary_detail_usecase.execute(request)
        
        # 권한 확인에서 실패하므로 후속 Repository 호출되지 않아야 함
        mock_week_topic_repository.find_by_id.assert_not_called()
        mock_curriculum_repository.find_by_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_week_topic_not_found(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_summary
    ):
        """연관된 주차 정보가 없을 때 에러"""
        # Given
        request = GetSummaryDetailRequest(
            summary_id=sample_summary.id,
            user_id=sample_summary.user_id
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=sample_summary)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=None)  # 주차 없음
        
        # When & Then
        with pytest.raises(ValueError, match="연관된 주차 정보를 찾을 수 없습니다"):
            await get_summary_detail_usecase.execute(request)
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_curriculum_not_found(
        self,
        get_summary_detail_usecase,
        mock_summary_repository,
        mock_week_topic_repository,
        mock_curriculum_repository,
        sample_summary,
        sample_week_topic
    ):
        """연관된 커리큘럼 정보가 없을 때 에러"""
        # Given
        request = GetSummaryDetailRequest(
            summary_id=sample_summary.id,
            user_id=sample_summary.user_id
        )
        
        mock_summary_repository.find_by_id = AsyncMock(return_value=sample_summary)
        mock_week_topic_repository.find_by_id = AsyncMock(return_value=sample_week_topic)
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=None)  # 커리큘럼 없음
        
        # When & Then
        with pytest.raises(ValueError, match="연관된 커리큘럼 정보를 찾을 수 없습니다"):
            await get_summary_detail_usecase.execute(request)