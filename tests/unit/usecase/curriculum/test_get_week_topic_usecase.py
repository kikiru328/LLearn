import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.curriculum.get_week_topic import GetWeekTopicUseCase
from usecase.dto.curriculum_dto import GetWeekTopicRequest, GetWeekTopicResponse

@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture
def mock_week_topic_repository():
    return Mock()

@pytest.fixture
def get_week_topic_usecase(mock_curriculum_repository, mock_week_topic_repository):
    return GetWeekTopicUseCase(
        curriculum_repository=mock_curriculum_repository,
        week_topic_repository=mock_week_topic_repository
    )

@pytest.fixture
def sample_curriculum():
    """Mock Curriculum 엔티티"""
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.user_id = uuid4()
    curriculum.title = "CS 기초 과정"
    curriculum.goal = "컴퓨터 과학 기초 이해"
    curriculum.is_public = False
    curriculum.created_at = datetime.now(timezone.utc)
    curriculum.updated_at = datetime.now(timezone.utc)
    return curriculum

@pytest.fixture
def sample_week_topic(sample_curriculum):
    """Mock WeekTopic 엔티티 - sample_curriculum과 연결됨"""
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = sample_curriculum.id  # ✅ 같은 ID 사용!
    week_topic.week_number = 1
    week_topic.title = "1주차: 컴퓨터구조 기초"
    week_topic.description = "컴퓨터의 기본 구조를 학습합니다"
    week_topic.learning_goals = ["CPU 이해", "메모리 구조 학습", "폰노이만 구조"]
    week_topic.created_at = datetime.now(timezone.utc)
    week_topic.updated_at = datetime.now(timezone.utc)
    return week_topic

@pytest.fixture
def public_curriculum():
    """공개 커리큘럼 (다른 사용자 소유)"""
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.user_id = uuid4()  # 다른 사용자 ID
    curriculum.title = "공개 파이썬 과정"
    curriculum.is_public = True  # 공개
    return curriculum

@pytest.fixture
def public_week_topic(public_curriculum):
    """공개 커리큘럼의 주차"""
    week_topic = Mock()
    week_topic.id = uuid4()
    week_topic.curriculum_id = public_curriculum.id  # ✅ 공개 커리큘럼과 연결
    week_topic.week_number = 1
    week_topic.title = "1주차: 파이썬 기초"
    week_topic.description = "파이썬 기본 문법"
    week_topic.learning_goals = ["변수", "자료형", "조건문"]
    week_topic.created_at = datetime.now(timezone.utc)
    week_topic.updated_at = datetime.now(timezone.utc)
    return week_topic

class TestGetWeekTopicUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_own_week_topic_successfully(
        self,
        get_week_topic_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        sample_curriculum,
        sample_week_topic
    ):
        """본인 커리큘럼의 주차 조회 성공"""
        # Given
        request = GetWeekTopicRequest(
            curriculum_id=sample_curriculum.id,
            week_number=1,
            user_id=sample_curriculum.user_id  # 본인 ID
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_week_topic_repository.find_by_curriculum_and_week = AsyncMock(return_value=sample_week_topic)
        
        # When
        result = await get_week_topic_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetWeekTopicResponse)
        assert result.id == sample_week_topic.id
        assert result.curriculum_id == sample_curriculum.id
        assert result.week_number == 1
        assert result.title == "1주차: 컴퓨터구조 기초"
        assert result.description == "컴퓨터의 기본 구조를 학습합니다"
        assert result.learning_goals == ["CPU 이해", "메모리 구조 학습", "폰노이만 구조"]
        assert result.curriculum_title == "CS 기초 과정"
        
        # Repository 호출 확인
        mock_curriculum_repository.find_by_id.assert_called_once_with(sample_curriculum.id)
        mock_week_topic_repository.find_by_curriculum_and_week.assert_called_once_with(
            sample_curriculum.id, 1
        )
    
    @pytest.mark.asyncio
    async def test_execute_returns_public_week_topic_successfully(
        self,
        get_week_topic_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        public_curriculum,
        public_week_topic
    ):
        """다른 사용자의 공개 커리큘럼 주차 조회 성공"""
        # Given
        different_user_id = uuid4()  # 다른 사용자
        request = GetWeekTopicRequest(
            curriculum_id=public_curriculum.id,
            week_number=1,
            user_id=different_user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=public_curriculum)
        mock_week_topic_repository.find_by_curriculum_and_week = AsyncMock(return_value=public_week_topic)
        
        # When
        result = await get_week_topic_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetWeekTopicResponse)
        assert result.title == "1주차: 파이썬 기초"
        assert result.curriculum_title == "공개 파이썬 과정"
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_curriculum_not_found(
        self,
        get_week_topic_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository
    ):
        """존재하지 않는 커리큘럼 조회 시 에러"""
        # Given
        request = GetWeekTopicRequest(
            curriculum_id=uuid4(),  # 존재하지 않는 ID
            week_number=1,
            user_id=uuid4()
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=None)  # 커리큘럼 없음
        
        # When & Then
        with pytest.raises(ValueError, match="커리큘럼을 찾을 수 없습니다"):
            await get_week_topic_usecase.execute(request)
        
        # find_by_curriculum_and_week는 호출되지 않아야 함
        mock_week_topic_repository.find_by_curriculum_and_week.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_week_topic_not_found(
        self,
        get_week_topic_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        sample_curriculum
    ):
        """존재하지 않는 주차 조회 시 에러"""
        # Given
        request = GetWeekTopicRequest(
            curriculum_id=sample_curriculum.id,
            week_number=99,  # 존재하지 않는 주차
            user_id=sample_curriculum.user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_week_topic_repository.find_by_curriculum_and_week = AsyncMock(return_value=None)  # 주차 없음
        
        # When & Then
        with pytest.raises(ValueError, match="99주차를 찾을 수 없습니다"):
            await get_week_topic_usecase.execute(request)
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_access_denied(
        self,
        get_week_topic_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository
    ):
        """다른 사용자의 비공개 커리큘럼 접근 시 에러"""
        # Given
        private_curriculum = Mock()
        private_curriculum.id = uuid4()
        private_curriculum.user_id = uuid4()  # 다른 사용자 소유
        private_curriculum.is_public = False  # 비공개
        
        different_user_id = uuid4()  # 요청하는 사용자 (다른 사람)
        
        request = GetWeekTopicRequest(
            curriculum_id=private_curriculum.id,
            week_number=1,
            user_id=different_user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=private_curriculum)
        
        # When & Then
        with pytest.raises(ValueError, match="접근 권한이 없습니다"):
            await get_week_topic_usecase.execute(request)
        
        # 권한 확인에서 실패하므로 week_topic 조회는 호출되지 않아야 함
        mock_week_topic_repository.find_by_curriculum_and_week.assert_not_called()