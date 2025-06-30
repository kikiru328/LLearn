from abc import ABC, abstractmethod
from typing import List


class LLMService(ABC):
    """LLM 관련 서비스 인터페이스"""
    
    @abstractmethod
    async def generate_feedback(
        self, 
        summary_content: str, 
        week_topic_title: str,
        week_topic_description: str,
        learning_goals: List[str]
    ) -> str:
        """학습 요약에 대한 5단계 피드백 생성
        
        Args:
            summary_content: 사용자가 작성한 학습 요약
            week_topic_title: 학습 주제 제목
            week_topic_description: 학습 주제 상세 설명  
            learning_goals: 해당 주차의 학습 목표 리스트
            
        Returns:
            5단계 구조화된 피드백 텍스트
        """
        pass
    
    @abstractmethod
    async def generate_curriculum(self, goal: str, duration_weeks: int = 12) -> dict:
        """학습 목표 기반 커리큘럼 생성 (나중에 사용)"""
        pass