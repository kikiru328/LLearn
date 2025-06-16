from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid

from infrastructure.persistence.sqlalchemy.base import Base

class PromptLogModel(Base):
    __tablename__ = "prompt_logs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    summary_id = Column(PG_UUID(as_uuid=True), ForeignKey("summaries.id", ondelete="CASCADE"), nullable=False)

    prompt = Column(String(4000), nullable=False)
    response = Column(String(4000), nullable=False)

    model_name = Column(String(50), nullable=False)  # 예: GPT-4, Claude, vLLM
    latency = Column(Float, nullable=False)  # 초 단위로 기록

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    summary = relationship("SummaryModel", backref="prompt_logs")