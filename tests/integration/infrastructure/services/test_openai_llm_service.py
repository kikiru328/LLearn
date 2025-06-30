import pytest
from unittest.mock import Mock, AsyncMock, patch

from infrastructure.services.openai_llm_service import OpenAILLMService


class TestOpenAILLMService:
    @pytest.fixture
    def llm_service(self):
        return OpenAILLMService(api_key="test-api-key", model="gpt-4o")
    
    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI')
    async def test_generate_feedback_calls_openai_correctly(self, mock_openai_client, llm_service):
        # Given
        mock_client_instance = Mock()
        mock_openai_client.return_value = mock_client_instance
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        1. ✅ 정확성 확인: 프로세스의 독립성에 대해 잘 이해하셨습니다
        2. 📝 누락 보충: 스레드와의 차이점을 추가로 설명드리겠습니다
        3. ⚠️ 오류 수정: 특별한 오류는 없습니다
        4. 🤔 심화 질문: 컨텍스트 스위칭 비용에 대해 어떻게 생각하시나요?
        5. 📚 확장 학습: IPC 메커니즘에 대해 학습해보세요
        """
        
        mock_client_instance.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # 실제 서비스 인스턴스 재생성 (mock이 적용되도록)
        service = OpenAILLMService(api_key="test-api-key")
        
        # When
        result = await service.generate_feedback(
            summary_content="프로세스는 독립적인 메모리 공간을 가집니다",
            week_topic_title="운영체제 기초",
            week_topic_description="프로세스와 스레드 개념 학습",
            learning_goals=["프로세스 이해", "스레드 이해"]
        )
        
        # Then
        assert "정확성 확인" in result
        assert "누락 보충" in result
        assert "오류 수정" in result
        assert "심화 질문" in result
        assert "확장 학습" in result
        
        # OpenAI API 호출 확인
        mock_client_instance.chat.completions.create.assert_called_once()
        call_args = mock_client_instance.chat.completions.create.call_args
        
        assert call_args.kwargs['model'] == "gpt-4o"
        assert len(call_args.kwargs['messages']) == 2
        assert "전문적인 CS 교육 멘토" in call_args.kwargs['messages'][0]['content']
        assert "운영체제 기초" in call_args.kwargs['messages'][1]['content']
    
    def test_build_feedback_prompt_includes_all_context(self, llm_service):
        # Given
        summary_content = "프로세스는 독립적입니다"
        week_topic_title = "운영체제"
        week_topic_description = "프로세스 개념"
        learning_goals = ["프로세스 이해", "스레드 이해"]
        
        # When
        prompt = llm_service._build_feedback_prompt(
            summary_content, week_topic_title, week_topic_description, learning_goals
        )
        
        # Then
        assert "운영체제" in prompt
        assert "프로세스 개념" in prompt
        assert "프로세스 이해, 스레드 이해" in prompt
        assert "프로세스는 독립적입니다" in prompt
        assert "✅ 정확성 확인" in prompt
        assert "📝 누락 보충" in prompt
        assert "⚠️ 오류 수정" in prompt
        assert "🤔 심화 질문" in prompt
        assert "📚 확장 학습" in prompt