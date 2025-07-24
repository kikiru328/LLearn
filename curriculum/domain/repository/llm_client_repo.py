from abc import ABCMeta, abstractmethod
from typing import Any, List, Dict


class ILLMClient(metaclass=ABCMeta):
    @abstractmethod
    async def generate_schedule(self, goal: str, weeks: int) -> List[Dict[str, Any]]:
        """
        주어진 목표(goal)와 주차 수(weeks)에 따른 학습 주차별 스케줄을 반환합니다.
        반환 형식 예시:
        [
            {"week_number": 1, "topics": ["Intro"]},
            {"week_number": 2, "topics": ["Deep Dive"]},
            ...
        ]
        """
        raise NotImplementedError
