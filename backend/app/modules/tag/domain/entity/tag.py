from dataclasses import dataclass
from datetime import datetime

from app.modules.tag.domain.vo.tag_name import TagName


@dataclass
class Tag:
    """태그 Entity"""

    id: str
    name: TagName
    usage_count: int
    created_by: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip():
            raise TypeError("id must be a non-empty string")
        if not isinstance(self.name, TagName):
            raise TypeError(f"name must be TagName, got {type(self.name).__name__}")
        if not isinstance(self.usage_count, int) or self.usage_count < 0:
            raise TypeError("usage_count must be a non-negative integer")
        if not isinstance(self.created_by, str) or not self.created_by.strip():
            raise TypeError("created_by must be a non-empty string")
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be datetime, got {type(self.updated_at).__name__}"
            )

    def increment_usage(self) -> None:
        """태그 사용 횟수 증가"""
        self.usage_count += 1
        self.updated_at = datetime.now()

    def decrement_usage(self) -> None:
        """태그 사용 횟수 감소"""
        if self.usage_count > 0:
            self.usage_count -= 1
            self.updated_at = datetime.now()

    def is_popular(self, threshold: int = 10) -> bool:
        """인기 태그인지 확인"""
        return self.usage_count >= threshold

    def __str__(self) -> str:
        return f"Tag({self.name.value})"

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name='{self.name.value}' usage={self.usage_count}>"
