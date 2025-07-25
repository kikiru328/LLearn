from dataclasses import dataclass
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.topics import Topics


@dataclass
class WeekSchedule:
    week_number: WeekNumber
    topics: Topics

    def __post_init__(self):
        if not isinstance(self.week_number, WeekNumber):
            raise TypeError(
                f"week_number must be a WeekNumber instance, got {type(self.week_number).__name__}"
            )
        if not isinstance(self.topics, Topics):
            raise TypeError(
                f"topics must be a Topics instance, got {type(self.topics).__name__}"
            )
