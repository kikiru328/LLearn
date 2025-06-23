from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import mapped_column, Mapped
from infrastructure.database.base import BaseModel


class FeedbackModel(BaseModel):
    __tablename__ = "feedbacks"

    summary_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("summaries.id"),
        nullable=False,
        comment="주차별 피드백"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="피드백 내용"
    )