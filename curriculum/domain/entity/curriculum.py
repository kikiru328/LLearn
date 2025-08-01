from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from curriculum.domain.value_object.visibility import Visibility
from curriculum.domain.value_object.title import Title
from curriculum.domain.entity.week_schedule import WeekSchedule


@dataclass
class Curriculum:
    id: str
    owner_id: str
    title: Title
    visibility: Visibility
    created_at: datetime
    updated_at: datetime
    week_schedules: List[WeekSchedule] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.owner_id, str):
            raise TypeError(f"owner_id must be str, got {type(self.owner_id).__name__}")
        if not isinstance(self.title, Title):
            raise TypeError(f"title must be Title, got {type(self.title).__name__}")
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be datetime, got {type(self.updated_at).__name__}"
            )
        if not isinstance(self.week_schedules, list) or any(
            not isinstance(w, WeekSchedule) for w in self.week_schedules
        ):
            raise TypeError("week_schedules must be List[WeekSchedule]")
