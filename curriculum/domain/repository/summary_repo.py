from abc import ABCMeta, abstractmethod
from typing import List
from curriculum.domain.entity.summary import Summary
from curriculum.domain.value_object.week_number import WeekNumber


class ISummaryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(
        self,
        curriculum_id: str,
        week_number: WeekNumber,
        summary: Summary,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_week(
        self,
        curriculum_id: str,
        week_number: WeekNumber,
    ) -> List[Summary]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        summary_id: str,
    ) -> None:
        raise NotImplementedError
