from sqlalchemy import DateTime, ForeignKey, String
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from user.infra.db_models.user import UserModel
    from curriculum.infra.db_models.week_schedule import WeekScheduleModel
    from curriculum.infra.db_models.summary import SummaryModel


class CurriculumModel(Base):
    __tablename__ = "curriculums"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(10), nullable=False, default="PRIVATE"
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="curricula",
        passive_deletes=True,
    )

    week_schedules: Mapped[list["WeekScheduleModel"]] = relationship(
        "WeekScheduleModel",
        back_populates="curriculum",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    summaries: Mapped[list["SummaryModel"]] = relationship(
        "SummaryModel",
        back_populates="curriculum",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
