import openai
from typing import List

from domain.services.llm_service import LLMService


class OpenAILLMService(LLMService):
    """OpenAI API를 사용한 LLM 서비스 구현체"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_feedback(
        self, 
        summary_content: str, 
        week_topic_title: str,
        week_topic_description: str,
        learning_goals: List[str]
    ) -> str:
        """학습 요약에 대한 5단계 피드백 생성"""
        
        # 5단계 피드백 프롬프트 구성
        prompt = self._build_feedback_prompt(
            summary_content, week_topic_title, week_topic_description, learning_goals
        )
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 전문적인 CS 교육 멘토입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def generate_curriculum(self, goal: str, duration_weeks: int = 12) -> dict:
        """학습 목표 기반 커리큘럼 생성"""
        # TODO: 나중에 구현
        return {"weeks": []}
    
    def _build_feedback_prompt(
        self, 
        summary_content: str, 
        week_topic_title: str,
        week_topic_description: str,
        learning_goals: List[str]
    ) -> str:
        """5단계 피드백 프롬프트 생성"""
        goals_text = ", ".join(learning_goals)
        
        return f"""
                학습 주제: "{week_topic_title}"
                주제 설명: {week_topic_description}
                학습 목표: {goals_text}

                사용자가 작성한 학습 요약:
                {summary_content}

                위 요약에 대해 다음 5단계 구조로 피드백을 제공해주세요:

                1. ✅ 정확성 확인: 올바르게 이해한 부분을 인정하고 격려
                2. 📝 누락 보충: 빠진 핵심 개념이나 중요한 내용 설명
                3. ⚠️ 오류 수정: 잘못 이해한 부분이 있다면 정정
                4. 🤔 심화 질문: 더 깊이 있는 이해를 위한 질문 제시
                5. 📚 확장 학습: 다음에 학습하면 좋을 관련 주제 제안

                각 단계는 명확히 구분하여 작성해주세요.
                """