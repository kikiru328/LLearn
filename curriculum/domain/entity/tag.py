from dataclasses import dataclass
from datetime import datetime

from curriculum.domain.value_object.tag_name import TagName


@dataclass
class Tag:
    id: str
    name: TagName
    usage_count: int  # 태그가 사용된 횟수
    created_by: str  # 태그를 처음 만든 사용자 ID
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.name, TagName):
            raise TypeError(f"name must be TagName, got {type(self.name).__name__}")
        if not isinstance(self.usage_count, int):
            raise TypeError(
                f"usage_count must be int, got {type(self.usage_count).__name__}"
            )
        if not isinstance(self.created_by, str):
            raise TypeError(
                f"created_by must be str, got {type(self.created_by).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be datetime, got {type(self.updated_at).__name__}"
            )

    def increment_usage(self):
        """태그 사용 횟수 증가"""
        self.usage_count += 1
        self.updated_at = datetime.now()

    def decrement_usage(self):
        """태그 사용 횟수 감소"""
        if self.usage_count > 0:
            self.usage_count -= 1
            self.updated_at = datetime.now()

    def is_popular(self, threshold: int = 10) -> bool:
        """인기 태그인지 확인"""
        return self.usage_count >= threshold
