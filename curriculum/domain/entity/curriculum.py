from dataclasses import dataclass
from datetime import datetime

from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.value_object.title import Title


@dataclass
class Curriculum:
    id: str
    owner_id: str
    title: Title
    created_at: datetime
    updated_at: datetime
    week_schedules: list[WeekSchedule]

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be a str instance, got {type(self.id).__name__}")

        if not isinstance(self.owner_id, str):
            raise TypeError(
                f"owner_id must be a str instance, got {type(self.owner_id).__name__}"
            )

        if not isinstance(self.title, Title):
            raise TypeError(
                f"title must be a Title instance, got {type(self.title).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be a datetime instance, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be a datetime instance, got {type(self.updated_at).__name__}"
            )
        if not isinstance(self.week_schedules, list) or any(
            not isinstance(ws, WeekSchedule) for ws in self.week_schedules
        ):
            raise TypeError("week_schedules must be a list of WeekSchedule instances")
