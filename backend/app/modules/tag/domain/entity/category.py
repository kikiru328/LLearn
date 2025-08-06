from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.modules.tag.domain.vo.category_name import CategoryName


@dataclass
class Category:
    """카테고리 Entity"""

    id: str
    name: CategoryName
    description: Optional[str]
    color: str  # 헥스 색상 코드
    icon: Optional[str]
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip():
            raise TypeError("id must be a non-empty string")
        if not isinstance(self.name, CategoryName):
            raise TypeError(
                f"name must be CategoryName, got {type(self.name).__name__}"
            )
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError(
                f"description must be str or None, got {type(self.description).__name__}"
            )
        if not isinstance(self.color, str) or not self.color.strip():
            raise TypeError("color must be a non-empty string")
        if self.icon is not None and not isinstance(self.icon, str):
            raise TypeError(f"icon must be str or None, got {type(self.icon).__name__}")
        if not isinstance(self.sort_order, int):
            raise TypeError(
                f"sort_order must be int, got {type(self.sort_order).__name__}"
            )
        if not isinstance(self.is_active, bool):
            raise TypeError(
                f"is_active must be bool, got {type(self.is_active).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be datetime, got {type(self.updated_at).__name__}"
            )

    def _touch_updated_at(self) -> None:
        """updated_at 갱신"""
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        """카테고리 활성화"""
        if not self.is_active:
            self.is_active = True
            self._touch_updated_at()

    def deactivate(self) -> None:
        """카테고리 비활성화"""
        if self.is_active:
            self.is_active = False
            self._touch_updated_at()

    def change_name(self, new_name: CategoryName) -> None:
        """카테고리 이름 변경"""
        if self.name != new_name:
            self.name = new_name
            self._touch_updated_at()

    def change_description(self, new_description: Optional[str]) -> None:
        """카테고리 설명 변경"""
        if self.description != new_description:
            self.description = new_description
            self._touch_updated_at()

    def change_color(self, new_color: str) -> None:
        """카테고리 색상 변경"""
        if self.color != new_color:
            self.color = new_color
            self._touch_updated_at()

    def change_sort_order(self, new_sort_order: int) -> None:
        """정렬 순서 변경"""
        if self.sort_order != new_sort_order:
            self.sort_order = new_sort_order
            self._touch_updated_at()

    def __str__(self) -> str:
        return f"Category({self.name.value})"

    def __repr__(self) -> str:
        return (
            f"<Category id={self.id} name='{self.name.value}' active={self.is_active}>"
        )
