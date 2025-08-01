from abc import ABCMeta, abstractmethod
from typing import Optional
from curriculum.domain.entity.feedback import Feedback


class IFeedbackRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, feedback: Feedback) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_summary_id(self, summary_id: str) -> Optional[Feedback]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError
