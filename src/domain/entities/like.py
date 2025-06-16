from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Like:
    id: UUID
    user_id: UUID
    target_type: str  # 'summary' or 'curriculum'
    target_id: UUID
    created_at: datetime