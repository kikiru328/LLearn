from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from curriculum.domain.value_object.category_name import CategoryName


@dataclass
class Category:
    id: str
    name: CategoryName
    description: Optional[str]
    color: str  # 헥스 색상 코드 (예: #FF5733)
    icon: Optional[str]  # 아이콘 이름 (예: "code", "design")
    sort_order: int  # 정렬 순서
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.name, CategoryName):
            raise TypeError(
                f"name must be CategoryName, got {type(self.name).__name__}"
            )
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError(
                f"description must be str or None, got {type(self.description).__name__}"
            )
        if not isinstance(self.color, str):
            raise TypeError(f"color must be str, got {type(self.color).__name__}")
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

    def activate(self):
        """카테고리 활성화"""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self):
        """카테고리 비활성화"""
        self.is_active = False
        self.updated_at = datetime.now()
