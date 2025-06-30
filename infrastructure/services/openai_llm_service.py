import json
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

    def _build_curriculum_prompt(self, goal: str, duration_weeks: int) -> str:
        return f"""
                    당신은 CS(Computer Science) 교육 전문가입니다.

                    학습 목표: {goal}
                    학습 기간: {duration_weeks}주

                    OSSU(Open Source Society University) CS 커리큘럼 구조를 참고하여 체계적인 학습 계획을 생성해주세요:
                    https://github.com/ossu/computer-science

                    **핵심 원칙:**
                    1. 기초 → 고급 순서 (Prerequisites 고려)
                    2. Core CS 분야 포함: Programming, Math, Systems, Theory, Applications
                    3. 한국 개발자 취업에 도움되는 실무 중심 구성
                    4. 각 주차별로 명확한 학습 목표 설정

                    **반드시 다음 JSON 형식으로만 응답해주세요:**
                    {{
                        "title": "구체적이고 매력적인 커리큘럼 제목",
                        "weeks": [
                            {{
                                "week_number": 1,
                                "title": "1주차: 구체적인 주제명",
                                "learning_goals": ["구체적인 학습목표1", "구체적인 학습목표2", "구체적인 학습목표3"]
                            }}
                        ]
                    }}

                    **요구사항:**
                    - 정확히 {duration_weeks}주차까지 생성
                    - 각 주차 learning_goals는 2-4개 (너무 많지 않게)
                    - 실무에서 바로 활용 가능한 내용 포함
                    - JSON 외 다른 텍스트 절대 포함 금지

                    예시 학습 목표: "프로세스와 스레드의 차이점 이해", "TCP/UDP 프로토콜 비교", "배열과 링크드리스트 구현"
                """
    
    async def generate_curriculum(self, goal: str, duration_weeks: int = 12) -> dict:
        """학습 목표 기반 커리큘럼 생성"""
        prompt = self._build_curriculum_prompt(goal, duration_weeks)
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 CS 교육 전문가입니다. 반드시 JSON 형식으로만 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 일관성을 위해 낮은 값
                max_tokens=2000
            )
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            
            # 기본 구조 검증
            if "title" not in result or "weeks" not in result:
                raise ValueError("응답에 필수 필드(title, weeks)가 없습니다")
            
            if len(result["weeks"]) != duration_weeks:
                raise ValueError(f"요청한 {duration_weeks}주와 응답 주차 수가 다릅니다")
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM 응답을 JSON으로 파싱할 수 없습니다: {e}")
        except Exception as e:
            raise RuntimeError(f"커리큘럼 생성 중 오류 발생: {e}")
    
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