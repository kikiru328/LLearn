from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from curriculum.domain.value_object.comment_content import CommentContent


@dataclass
class Comment:
    id: str
    user_id: str
    curriculum_id: str
    content: CommentContent
    parent_comment_id: Optional[str]  # 대댓글용
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.user_id, str):
            raise TypeError(f"user_id must be str, got {type(self.user_id).__name__}")
        if not isinstance(self.curriculum_id, str):
            raise TypeError(
                f"curriculum_id must be str, got {type(self.curriculum_id).__name__}"
            )
        if not isinstance(self.content, CommentContent):
            raise TypeError(
                f"content must be CommentContent, got {type(self.content).__name__}"
            )
        if self.parent_comment_id is not None and not isinstance(
            self.parent_comment_id, str
        ):
            raise TypeError(
                f"parent_comment_id must be str or None, got {type(self.parent_comment_id).__name__}"
            )
        if not isinstance(self.is_deleted, bool):
            raise TypeError(
                f"is_deleted must be bool, got {type(self.is_deleted).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
        if not isinstance(self.updated_at, datetime):
            raise TypeError(
                f"updated_at must be datetime, got {type(self.updated_at).__name__}"
            )

    def is_reply(self) -> bool:
        """대댓글인지 확인"""
        return self.parent_comment_id is not None

    def soft_delete(self):
        """소프트 삭제"""
        self.is_deleted = True
        self.updated_at = datetime.now()
