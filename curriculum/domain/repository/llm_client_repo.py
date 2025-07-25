from abc import ABCMeta, abstractmethod
from typing import Any, List, Dict


class ILLMClient(metaclass=ABCMeta):
    @abstractmethod
    async def generate_schedule(self, goal: str, weeks: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def generate_feedback(
        self, topics: list[str], summary_content: str
    ) -> Dict[str, object]:
        # OpenAI API 호출로 피드백 생성
        pass
