from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List


class ILLMClientRepository(metaclass=ABCMeta):
    @abstractmethod
    async def generate(self, prompt: str, timeout: float | None = None) -> str:
        """Prompt을 보내고 raw 응답 문자열(JSON 등)을 반환"""
        raise NotImplementedError

    @abstractmethod
    async def generate_feedback(
        self, topics: List[str], summary_content: str, timeout: float | None = 10.0
    ) -> Dict[str, Any]:
        raise NotImplementedError
