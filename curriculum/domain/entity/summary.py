from dataclasses import dataclass
from datetime import datetime
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.summary_content import SummaryContent


@dataclass
class Summary:
    id: str
    curriculum_id: str
    week_number: WeekNumber
    content: SummaryContent
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.curriculum_id, str):
            raise TypeError(
                f"curriculum_id must be str, got {type(self.curriculum_id).__name__}"
            )
        if not isinstance(self.week_number, WeekNumber):
            raise TypeError(
                f"week_number must be WeekNumber, got {type(self.week_number).__name__}"
            )
        if not isinstance(self.content, SummaryContent):
            raise TypeError(
                f"content must be SummaryContent, got {type(self.content).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
