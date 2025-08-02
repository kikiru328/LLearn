from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curriculum.infra.db_models.curriculum import CurriculumModel
    from curriculum.infra.db_models.tag import TagModel
    from curriculum.infra.db_models.category import CategoryModel
    from user.infra.db_models.user import UserModel


class CurriculumTagModel(Base):
    __tablename__ = "curriculum_tags"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    curriculum_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )
    added_by: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 중복 방지: 같은 커리큘럼에 같은 태그 중복 연결 방지
    __table_args__ = (
        UniqueConstraint("curriculum_id", "tag_id", name="unique_curriculum_tag"),
        Index("idx_curriculum_tag_curriculum", "curriculum_id"),
        Index("idx_curriculum_tag_tag", "tag_id"),
        Index("idx_curriculum_tag_added_by", "added_by"),
    )

    # 관계 설정
    curriculum: Mapped["CurriculumModel"] = relationship(
        "CurriculumModel",
        passive_deletes=True,
    )
    tag: Mapped["TagModel"] = relationship(
        "TagModel",
        passive_deletes=True,
    )
    added_by_user: Mapped["UserModel"] = relationship(
        "UserModel",
        passive_deletes=True,
    )


class CurriculumCategoryModel(Base):
    __tablename__ = "curriculum_categories"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    curriculum_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("curriculums.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    assigned_by: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 제약 조건: 한 커리큘럼은 하나의 카테고리만 가질 수 있음
    __table_args__ = (
        UniqueConstraint("curriculum_id", name="unique_curriculum_category"),
        Index("idx_curriculum_category_curriculum", "curriculum_id"),
        Index("idx_curriculum_category_category", "category_id"),
        Index("idx_curriculum_category_assigned_by", "assigned_by"),
    )

    # 관계 설정
    curriculum: Mapped["CurriculumModel"] = relationship(
        "CurriculumModel",
        passive_deletes=True,
    )
    category: Mapped["CategoryModel"] = relationship(
        "CategoryModel",
        passive_deletes=True,
    )
    assigned_by_user: Mapped["UserModel"] = relationship(
        "UserModel",
        passive_deletes=True,
    )
