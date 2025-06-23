from sqlalchemy import String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import BaseModel
from typing import List
class WeekTopicModel(BaseModel):
    """week topic model"""
    __tablename__ = "week_topics"

    curriculum_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("curriculums.id"),
        nullable=False,
        comment="커리큘럼 ID"
    )

    week_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="학습 주차"
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="주차 별 제목"
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        comment="주차 별 설명"
    )

    learning_goals: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        comment="학습 내용"
    )




