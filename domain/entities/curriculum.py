from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class Curriculum:
    """Curriculum domain entity"""
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    title: str
    goal: str
    duration_weeks: int
    is_public: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_title(self, new_title: str) -> None:
        """modify title"""
        if not new_title or len(new_title.strip()) < 2:
            raise ValueError("커리큘럼 제목은 2자 이상이어야 합니다.")
        self.title = new_title.strip()
        self.updated_at = datetime.now(timezone.utc)

    def make_public(self) -> None:
        """open curriculum to public"""
        self.is_public = True
        self.updated_at = datetime.now(timezone.utc)

    def make_private(self) -> None:
        """set curriculum to public"""
        self.is_public = False
        self.updated_at = datetime.now(timezone.utc)