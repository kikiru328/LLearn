from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class PromptLog:
    id: UUID
    summary_id: UUID
    prompt: str
    response: str
    model_name: str
    latency: float
    created_at: datetime