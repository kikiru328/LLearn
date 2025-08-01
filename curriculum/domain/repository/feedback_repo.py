from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple
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

    @abstractmethod
    async def find_all_feedbacks_for_admin(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Feedback]]:
        raise NotImplementedError

    async def count_all(self) -> int:
        raise NotImplementedError
