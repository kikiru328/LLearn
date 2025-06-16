from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Summary:
    id: UUID
    user_id: UUID
    curriculum_id: UUID
    week_number: int
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime

    def update_content(self, new_content: str) -> None:
        """Update summary content"""
        self.content = new_content
        self.updated_at = datetime.now()

    def toggle_visibility(self) -> None:
        """Toggle public/private status"""
        self.is_public = not self.is_public
        self.updated_at = datetime.now()