from sqlalchemy import String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import BaseModel

class SummaryModel(BaseModel):
    __tablename__ = "summaries"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        comment="사용자 ID"
    )

    week_topic_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("week_topics.id"),
        nullable=False,
        comment="주차별 ID"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        comment="주차 별 요약본"
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True, # lot of query
        comment="공개 상태"
    )