import pytest
from unittest.mock import Mock, AsyncMock

from usecase.curriculum.generate_preview import GenerateCurriculumPreviewUseCase
from usecase.dto.curriculum_dto import GeneratePreviewRequest, GeneratePreviewResponse

@pytest.fixture
def mock_llm_service():
    return Mock()

@pytest.fixture
def generate_preview_usecase(mock_llm_service):
    return GenerateCurriculumPreviewUseCase(llm_service=mock_llm_service)

@pytest.fixture
def sample_llm_response():
    return {
        "title": "파이썬 마스터하기 4주 과정",
        "weeks": [
            {
                "week_number": 1,
                "title": "1주차: 파이썬 기초",
                "learning_goals": ["파이썬이란?", "변수와 자료형"]
            },
            {
                "week_number": 2,
                "title": "2주차: 제어문과 함수",
                "learning_goals": ["조건문", "반복문", "함수 정의"]
            }
        ]
    }

class TestGenerateCurriculumPreviewUseCase:
    @pytest.mark.asyncio
    async def test_execute_generates_preview_successfully(
        self,
        generate_preview_usecase,
        mock_llm_service,
        sample_llm_response
    ):
        # Given
        request = GeneratePreviewRequest(
            goal="파이썬을 처음부터 끝까지 완전히 마스터하고 싶습니다. 기초부터 고급까지 모든 것을 배우고 싶어요.",
            duration_weeks=4
        )
        
        mock_llm_service.generate_curriculum = AsyncMock(return_value=sample_llm_response)
        
        # When
        result = await generate_preview_usecase.execute(request)
        
        # Then
        assert isinstance(result, GeneratePreviewResponse)
        assert result.title == "파이썬 마스터하기 4주 과정"
        assert result.goal == request.goal
        assert result.duration_weeks == 4
        assert len(result.weeks) == 2
        
        # WeekTopicData 검증
        assert result.weeks[0].week_number == 1
        assert result.weeks[0].title == "1주차: 파이썬 기초"
        assert result.weeks[0].description == ""  # 빈 문자열
        assert result.weeks[0].learning_goals == ["파이썬이란?", "변수와 자료형"]
        
        # LLM 서비스 호출 검증
        mock_llm_service.generate_curriculum.assert_called_once_with(
            goal=request.goal,
            duration_weeks=request.duration_weeks
        )