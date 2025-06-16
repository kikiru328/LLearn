from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import List

@dataclass
class WeekTopic:
    week_number: int
    topic: str

@dataclass
class Curriculum:
    id: UUID
    user_id: UUID
    title: str
    goal: str
    is_public: bool
    weeks: List[WeekTopic]
    created_at: datetime
    updated_at: datetime

    def change_title(self, new_title: str) -> None:
        """Change curriculum title to new_title."""
        self.title = new_title
        self.updated_at = datetime.now()

    def update_goal(self, new_goal: str) -> None:
        """Update the learning goal of the curriculum."""
        self.goal = new_goal
        self.updated_at = datetime.now()

    def toggle_visibility(self) -> None:
        """Toggle curriculum visibility (public/private)."""
        self.is_public = not self.is_public
        self.updated_at = datetime.now()
