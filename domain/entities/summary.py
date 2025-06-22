from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class Summary:
    """summary entity"""
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_content(self, new_content: str) -> None:
        """change summary contents"""
        if not new_content or len(new_content.strip()) < 10:
            raise ValueError("요약 내용은 10자 이상이어야 합니다.")
        self.content = new_content.strip()
        self.updated_at = datetime.now(timezone.utc)

    def make_public(self) -> None:
        """summary to public"""
        self.is_public = True
        self.updated_at = datetime.now(timezone.utc)

    def make_private(self) -> None:
        """summary to private"""
        self.is_public = False
        self.updated_at = datetime.now(timezone.utc)