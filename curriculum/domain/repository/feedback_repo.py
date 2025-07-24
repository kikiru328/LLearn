from abc import ABCMeta, abstractmethod
from ulid import ULID
from typing import List
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.value_object.week_number import WeekNumber


class IFeedbackRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(
        self,
        curriculum_id: ULID,
        week_number: WeekNumber,
        summary_id: ULID,
        feedback: Feedback,
    ) -> None:
        """주어진 커리큘럼과 주차에 대한 피드백을 저장합니다."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_week(
        self,
        curriculum_id: ULID,
        week_number: WeekNumber,
    ) -> List[Feedback]:
        """특정 커리큘럼의 지정된 주차에 제출된 모든 피드백을 반환합니다."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        curriculum_id: ULID,
    ) -> List[Feedback]:
        """특정 커리큘럼에 달린 모든 피드백을 반환합니다."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_summary(
        self,
        summary_id: ULID,
    ) -> None:
        """주어진 요약 ID에 연관된 모든 피드백을 삭제합니다."""
        raise NotImplementedError
