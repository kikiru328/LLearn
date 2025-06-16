from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PromptLogListItem(BaseModel):
    id: UUID
    summary_id: UUID
    model_name: str
    latency: float
    created_at: datetime

class PromptLogDetailResponse(BaseModel):
    id: UUID
    summary_id: UUID
    prompt: str
    response: str
    model_name: str
    latency: float
    created_at: datetime