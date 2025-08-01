from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bookmark:
    id: str
    user_id: str
    curriculum_id: str
    created_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.user_id, str):
            raise TypeError(f"user_id must be str, got {type(self.user_id).__name__}")
        if not isinstance(self.curriculum_id, str):
            raise TypeError(
                f"curriculum_id must be str, got {type(self.curriculum_id).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
