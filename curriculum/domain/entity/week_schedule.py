from dataclasses import dataclass
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.lessons import Lessons


@dataclass
class WeekSchedule:
    week_number: WeekNumber
    lessons: Lessons

    def __post_init__(self):
        if not isinstance(self.week_number, WeekNumber):
            raise TypeError(
                f"week_number must be WeekNumber, got {type(self.week_number).__name__}"
            )
        if not isinstance(self.lessons, Lessons):
            raise TypeError(
                f"lessons must be Lessons, got {type(self.lessons).__name__}"
            )
