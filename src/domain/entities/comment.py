from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Comment:
    id: UUID
    user_id: UUID
    summary_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    def edit(self, new_content: str) -> None:
        """Update comment content"""
        self.content = new_content
        self.updated_at = datetime.now()