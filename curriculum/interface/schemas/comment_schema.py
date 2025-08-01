from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from curriculum.domain.entity.comment import Comment


class CreateCommentRequest(BaseModel):
    """댓글 작성 요청"""

    content: str = Field(min_length=1, max_length=1000, description="댓글 내용")
    parent_comment_id: Optional[str] = Field(
        None, description="대댓글인 경우 부모 댓글 ID"
    )


class UpdateCommentRequest(BaseModel):
    """댓글 수정 요청"""

    content: str = Field(min_length=1, max_length=1000, description="수정할 댓글 내용")


class CommentResponse(BaseModel):
    """댓글 응답"""

    id: str
    user_id: str
    curriculum_id: str
    content: str
    parent_comment_id: Optional[str]
    is_deleted: bool
    reply_count: int = 0  # 대댓글 수
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, comment: Comment, reply_count: int = 0) -> "CommentResponse":
        return cls(
            id=comment.id,
            user_id=comment.user_id,
            curriculum_id=comment.curriculum_id,
            content=comment.content.value,
            parent_comment_id=comment.parent_comment_id,
            is_deleted=comment.is_deleted,
            reply_count=reply_count,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class CommentPageResponse(BaseModel):
    """댓글 목록 페이지 응답"""

    total_count: int
    page: int
    items_per_page: int
    comments: List[CommentResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        comments: List[Comment],
        page: int,
        items_per_page: int,
        reply_counts: List[int] = None,
    ) -> "CommentPageResponse":
        if reply_counts is None:
            reply_counts = [0] * len(comments)

        comment_responses = [
            CommentResponse.from_domain(comment, reply_count)
            for comment, reply_count in zip(comments, reply_counts)
        ]

        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            comments=comment_responses,
        )


class CurriculumCommentStatsResponse(BaseModel):
    """커리큘럼 댓글 통계 응답"""

    curriculum_id: str
    total_comment_count: int  # 전체 댓글 수 (대댓글 포함)
