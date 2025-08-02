from dataclasses import dataclass
from datetime import datetime


@dataclass
class CurriculumTag:
    """커리큘럼과 태그의 연결 테이블"""

    id: str
    curriculum_id: str
    tag_id: str
    added_by: str  # 태그를 추가한 사용자 ID
    created_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.curriculum_id, str):
            raise TypeError(
                f"curriculum_id must be str, got {type(self.curriculum_id).__name__}"
            )
        if not isinstance(self.tag_id, str):
            raise TypeError(f"tag_id must be str, got {type(self.tag_id).__name__}")
        if not isinstance(self.added_by, str):
            raise TypeError(f"added_by must be str, got {type(self.added_by).__name__}")
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )


@dataclass
class CurriculumCategory:
    """커리큘럼과 카테고리의 연결 테이블"""

    id: str
    curriculum_id: str
    category_id: str
    assigned_by: str  # 카테고리를 할당한 사용자 ID
    created_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.curriculum_id, str):
            raise TypeError(
                f"curriculum_id must be str, got {type(self.curriculum_id).__name__}"
            )
        if not isinstance(self.category_id, str):
            raise TypeError(
                f"category_id must be str, got {type(self.category_id).__name__}"
            )
        if not isinstance(self.assigned_by, str):
            raise TypeError(
                f"assigned_by must be str, got {type(self.assigned_by).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
