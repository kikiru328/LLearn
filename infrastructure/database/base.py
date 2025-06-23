from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import MetaData, String, DateTime, func
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 네이밍 컨벤션 설정
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    """모든 SQLAlchemy 모델의 기본 클래스"""
    metadata = MetaData(naming_convention=convention)


class BaseModel(Base):
    """공통 컬럼을 가진 기본 모델"""
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        CHAR(36),  # MySQL UUID는 문자열로 저장
        primary_key=True,
        default=lambda: str(uuid4()),  # 문자열로 변환
        comment="기본키"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="생성일시"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="수정일시"
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"