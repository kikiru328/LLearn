from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curriculum.infra.db_models.curriculum import CurriculumModel
    from curriculum.infra.db_models.feedback import FeedbackModel


class SummaryModel(Base):
    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    curriculum_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 역방향 관계
    curriculum: Mapped["CurriculumModel"] = relationship(
        "CurriculumModel",
        back_populates="summaries",
        passive_deletes=True,
    )
    feedbacks: Mapped[list["FeedbackModel"]] = relationship(
        "FeedbackModel",
        back_populates="summary",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
