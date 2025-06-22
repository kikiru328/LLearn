from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class Feedback:
    """AI Feedback entity"""
    id: UUID = field(default_factory=uuid4)
    summary_id: UUID
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))