from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class WeekTopic:
    id: UUID = field(default_factory=uuid4)
    curriculum_id: UUID
    week_number: int
    title: str
    description: str
    learning_goals: List[str]
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_title(self, new_title: str) -> None:
        """change title"""
        if not new_title or len(new_title.strip()) < 2:
            raise ValueError("주제 제목은 2자 이상이어야 합니다.")
        self.title = new_title.strip()
        self.updated_at = datetime.now(timezone.utc)

    def update_description(self, new_description: str) -> None:
        """modify description"""
        if not new_description or len(new_description.strip()) < 10:
            raise ValueError("주제 설명은 10자 이상이어야 합니다.")
        self.description = new_description.strip()
        self.updated_at = datetime.now(timezone.utc)

    def update_learning_goals(self, new_goals: List[str]) -> None:
        """modeify learning goals"""
        if not new_goals or len(new_goals) == 0:
            raise ValueError("학습 내용은 최소 1개 이상이어야 합니다.")
        self.learning_goals = new_goals
        self.updated_at = datetime.now(timezone.utc)