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
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_title(self, new_title: str) -> None:
        """change title"""
        if not new_title or new_title.strip() == "":
            self.title = f"{self.week_number}주차"
        else:
            self.title = new_title.strip()
        self.updated_at = datetime.now(timezone.utc)

    def update_description(self, new_description: str) -> None:
        """modify description"""
        self.description = new_description.strip() # 빈 문장도 가능
        self.updated_at = datetime.now(timezone.utc)

    def update_learning_goals(self, new_goals: List[str]) -> None:
        """modeify learning goals"""
        if not new_goals or len(new_goals) == 0:
            raise ValueError("학습 내용은 최소 1개 이상이어야 합니다.")
        self.learning_goals = new_goals
        self.updated_at = datetime.now(timezone.utc)