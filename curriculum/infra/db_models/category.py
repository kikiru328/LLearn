from sqlalchemy import String, Text, Boolean, Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False)  # 헥스 색상 (#FFFFFF)
    icon: Mapped[str] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # 인덱스 설정
    __table_args__ = (
        Index("idx_category_active_sort", "is_active", "sort_order"),
        Index("idx_category_name", "name"),
    )
