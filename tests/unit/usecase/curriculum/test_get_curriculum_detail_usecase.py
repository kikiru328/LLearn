import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime, timezone

from usecase.curriculum.get_curriculum_detail import GetCurriculumDetailUseCase
from usecase.dto.curriculum_dto import GetCurriculumDetailRequest, GetCurriculumDetailResponse, WeekTopicData

@pytest.fixture
def mock_curriculum_repository():
    return Mock()

@pytest.fixture  
def mock_week_topic_repository():
    return Mock()

@pytest.fixture
def get_curriculum_detail_usecase(mock_curriculum_repository, mock_week_topic_repository):
    return GetCurriculumDetailUseCase(
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
    curriculum.goal = "컴퓨터 과학 기초를 체계적으로 학습하여 개발자로서의 기반을 다지겠습니다"
    curriculum.duration_weeks = 3
    curriculum.is_public = False
    curriculum.created_at = datetime.now(timezone.utc)
    curriculum.updated_at = datetime.now(timezone.utc)
    return curriculum

@pytest.fixture
def sample_week_topics(sample_curriculum):
    """Mock WeekTopic 엔티티들 - sample_curriculum과 연결됨"""
    week_topic1 = Mock()
    week_topic1.id = uuid4()
    week_topic1.curriculum_id = sample_curriculum.id  
    week_topic1.week_number = 1
    week_topic1.title = "1주차: 컴퓨터구조 기초"
    week_topic1.description = "컴퓨터의 기본 구조 학습"
    week_topic1.learning_goals = ["CPU 이해", "메모리 구조", "폰노이만 구조"]
    week_topic1.created_at = datetime.now(timezone.utc)
    week_topic1.updated_at = datetime.now(timezone.utc)
    
    week_topic2 = Mock()
    week_topic2.id = uuid4()
    week_topic2.curriculum_id = sample_curriculum.id  
    week_topic2.week_number = 2
    week_topic2.title = "2주차: 운영체제 기초"
    week_topic2.description = "운영체제 핵심 개념 학습"
    week_topic2.learning_goals = ["프로세스", "스레드", "메모리 관리"]
    week_topic2.created_at = datetime.now(timezone.utc)
    week_topic2.updated_at = datetime.now(timezone.utc)
    
    week_topic3 = Mock()
    week_topic3.id = uuid4()
    week_topic3.curriculum_id = sample_curriculum.id  
    week_topic3.week_number = 3
    week_topic3.title = "3주차: 자료구조 기초"
    week_topic3.description = "기본 자료구조들 학습"
    week_topic3.learning_goals = ["배열", "링크드리스트", "스택과 큐"]
    week_topic3.created_at = datetime.now(timezone.utc)
    week_topic3.updated_at = datetime.now(timezone.utc)
    
    return [week_topic1, week_topic2, week_topic3]

@pytest.fixture
def public_curriculum():
    """공개 커리큘럼 (다른 사용자 소유)"""
    curriculum = Mock()
    curriculum.id = uuid4()
    curriculum.user_id = uuid4()  # 다른 사용자 ID
    curriculum.title = "공개 파이썬 마스터 과정"
    curriculum.goal = "파이썬을 완전히 마스터하기 위한 체계적인 학습"
    curriculum.duration_weeks = 2
    curriculum.is_public = True  # 공개
    curriculum.created_at = datetime.now(timezone.utc)
    curriculum.updated_at = datetime.now(timezone.utc)
    return curriculum

@pytest.fixture
def public_week_topics(public_curriculum):
    """공개 커리큘럼의 주차들"""
    week_topic1 = Mock()
    week_topic1.id = uuid4()
    week_topic1.curriculum_id = public_curriculum.id  
    week_topic1.week_number = 1
    week_topic1.title = "1주차: 파이썬 기초"
    week_topic1.description = "파이썬 기본 문법"
    week_topic1.learning_goals = ["변수", "자료형", "조건문"]
    week_topic1.created_at = datetime.now(timezone.utc)
    week_topic1.updated_at = datetime.now(timezone.utc)
    
    week_topic2 = Mock()
    week_topic2.id = uuid4()
    week_topic2.curriculum_id = public_curriculum.id  
    week_topic2.week_number = 2
    week_topic2.title = "2주차: 파이썬 고급"
    week_topic2.description = "파이썬 고급 기능들"
    week_topic2.learning_goals = ["클래스", "상속", "모듈"]
    week_topic2.created_at = datetime.now(timezone.utc)
    week_topic2.updated_at = datetime.now(timezone.utc)
    
    return [week_topic1, week_topic2]

class TestGetCurriculumDetailUseCase:
    @pytest.mark.asyncio
    async def test_execute_returns_own_curriculum_successfully(
        self,
        get_curriculum_detail_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        sample_curriculum,
        sample_week_topics
    ):
        """본인 커리큘럼 상세 조회 성공"""
        # Given
        request = GetCurriculumDetailRequest(
            curriculum_id=sample_curriculum.id,
            user_id=sample_curriculum.user_id  # 본인 ID
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_week_topic_repository.find_by_curriculum_id = AsyncMock(return_value=sample_week_topics)
        
        # When
        result = await get_curriculum_detail_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetCurriculumDetailResponse)
        assert result.id == sample_curriculum.id
        assert result.user_id == sample_curriculum.user_id
        assert result.title == "CS 기초 과정"
        assert result.goal == "컴퓨터 과학 기초를 체계적으로 학습하여 개발자로서의 기반을 다지겠습니다"
        assert result.duration_weeks == 3
        assert result.is_public == False
        
        # 주차별 데이터 검증 (정렬되어 있어야 함)
        assert len(result.weeks) == 3
        assert result.weeks[0].week_number == 1
        assert result.weeks[0].title == "1주차: 컴퓨터구조 기초"
        assert result.weeks[0].learning_goals == ["CPU 이해", "메모리 구조", "폰노이만 구조"]
        
        assert result.weeks[1].week_number == 2
        assert result.weeks[1].title == "2주차: 운영체제 기초"
        
        assert result.weeks[2].week_number == 3
        assert result.weeks[2].title == "3주차: 자료구조 기초"
        
        # Repository 호출 확인
        mock_curriculum_repository.find_by_id.assert_called_once_with(sample_curriculum.id)
        mock_week_topic_repository.find_by_curriculum_id.assert_called_once_with(sample_curriculum.id)
    
    @pytest.mark.asyncio  
    async def test_execute_returns_public_curriculum_successfully(
        self,
        get_curriculum_detail_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        public_curriculum,
        public_week_topics
    ):
        """다른 사용자의 공개 커리큘럼 조회 성공"""
        # Given
        different_user_id = uuid4()  # 다른 사용자
        request = GetCurriculumDetailRequest(
            curriculum_id=public_curriculum.id,
            user_id=different_user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=public_curriculum)
        mock_week_topic_repository.find_by_curriculum_id = AsyncMock(return_value=public_week_topics)
        
        # When
        result = await get_curriculum_detail_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetCurriculumDetailResponse)
        assert result.title == "공개 파이썬 마스터 과정"
        assert result.is_public == True
        assert len(result.weeks) == 2
        assert result.weeks[0].title == "1주차: 파이썬 기초"
        assert result.weeks[1].title == "2주차: 파이썬 고급"
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_curriculum_not_found(
        self,
        get_curriculum_detail_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository
    ):
        """존재하지 않는 커리큘럼 조회 시 에러"""
        # Given
        request = GetCurriculumDetailRequest(
            curriculum_id=uuid4(),  # 존재하지 않는 ID
            user_id=uuid4()
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=None)  # 커리큘럼 없음
        
        # When & Then
        with pytest.raises(ValueError, match="커리큘럼을 찾을 수 없습니다"):
            await get_curriculum_detail_usecase.execute(request)
        
        # find_by_curriculum_id는 호출되지 않아야 함
        mock_week_topic_repository.find_by_curriculum_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_access_denied(
        self,
        get_curriculum_detail_usecase,
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
        
        request = GetCurriculumDetailRequest(
            curriculum_id=private_curriculum.id,
            user_id=different_user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=private_curriculum)
        
        # When & Then
        with pytest.raises(ValueError, match="접근 권한이 없습니다"):
            await get_curriculum_detail_usecase.execute(request)
        
        # 권한 확인에서 실패하므로 week_topics 조회는 호출되지 않아야 함
        mock_week_topic_repository.find_by_curriculum_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_returns_empty_weeks_when_no_week_topics(
        self,
        get_curriculum_detail_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        sample_curriculum
    ):
        """주차가 없는 커리큘럼 조회 (빈 리스트 반환)"""
        # Given
        request = GetCurriculumDetailRequest(
            curriculum_id=sample_curriculum.id,
            user_id=sample_curriculum.user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_week_topic_repository.find_by_curriculum_id = AsyncMock(return_value=[])  # 빈 리스트
        
        # When
        result = await get_curriculum_detail_usecase.execute(request)
        
        # Then
        assert isinstance(result, GetCurriculumDetailResponse)
        assert result.title == "CS 기초 과정"
        assert len(result.weeks) == 0  # 빈 리스트
    
    @pytest.mark.asyncio
    async def test_execute_sorts_weeks_by_week_number(
        self,
        get_curriculum_detail_usecase,
        mock_curriculum_repository,
        mock_week_topic_repository,
        sample_curriculum
    ):
        """주차들이 week_number 순서대로 정렬되는지 확인"""
        # Given
        # 의도적으로 순서를 섞은 주차들
        unordered_week_topics = []
        
        week_topic3 = Mock()
        week_topic3.week_number = 3
        week_topic3.title = "3주차"
        week_topic3.description = ""
        week_topic3.learning_goals = []
        
        week_topic1 = Mock()
        week_topic1.week_number = 1
        week_topic1.title = "1주차"
        week_topic1.description = ""
        week_topic1.learning_goals = []
        
        week_topic2 = Mock()
        week_topic2.week_number = 2
        week_topic2.title = "2주차"
        week_topic2.description = ""
        week_topic2.learning_goals = []
        
        unordered_week_topics = [week_topic3, week_topic1, week_topic2]  # 3, 1, 2 순서
        
        request = GetCurriculumDetailRequest(
            curriculum_id=sample_curriculum.id,
            user_id=sample_curriculum.user_id
        )
        
        mock_curriculum_repository.find_by_id = AsyncMock(return_value=sample_curriculum)
        mock_week_topic_repository.find_by_curriculum_id = AsyncMock(return_value=unordered_week_topics)
        
        # When
        result = await get_curriculum_detail_usecase.execute(request)
        
        # Then
        assert len(result.weeks) == 3
        # 정렬되어서 1, 2, 3 순서가 되어야 함
        assert result.weeks[0].week_number == 1
        assert result.weeks[0].title == "1주차"
        assert result.weeks[1].week_number == 2
        assert result.weeks[1].title == "2주차"
        assert result.weeks[2].week_number == 3
        assert result.weeks[2].title == "3주차"