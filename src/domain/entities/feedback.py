from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Feedback:
    id: UUID
    summary_id: UUID
    reviewer: str      # 예: "ChatGPT", "GPT-4", "vLLM"
    content: str       # 실제 피드백 텍스트
    created_at: datetime