from datetime import datetime
from typing import List
from pydantic import BaseModel

from curriculum.domain.entity.like import Like
from curriculum.domain.entity.bookmark import Bookmark


class LikeToggleResponse(BaseModel):
    """좋아요 토글 응답"""

    is_liked: bool
    like_count: int


class BookmarkToggleResponse(BaseModel):
    """북마크 토글 응답"""

    is_bookmarked: bool


class LikeResponse(BaseModel):
    """좋아요 정보"""

    id: str
    user_id: str
    curriculum_id: str
    created_at: datetime

    @classmethod
    def from_domain(cls, like: Like) -> "LikeResponse":
        return cls(
            id=like.id,
            user_id=like.user_id,
            curriculum_id=like.curriculum_id,
            created_at=like.created_at,
        )


class BookmarkResponse(BaseModel):
    """북마크 정보"""

    id: str
    user_id: str
    curriculum_id: str
    created_at: datetime

    @classmethod
    def from_domain(cls, bookmark: Bookmark) -> "BookmarkResponse":
        return cls(
            id=bookmark.id,
            user_id=bookmark.user_id,
            curriculum_id=bookmark.curriculum_id,
            created_at=bookmark.created_at,
        )


class LikePageResponse(BaseModel):
    """좋아요 목록 페이지 응답"""

    total_count: int
    page: int
    items_per_page: int
    likes: List[LikeResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        likes: List[Like],
        page: int,
        items_per_page: int,
    ) -> "LikePageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            likes=[LikeResponse.from_domain(like) for like in likes],
        )


class BookmarkPageResponse(BaseModel):
    """북마크 목록 페이지 응답"""

    total_count: int
    page: int
    items_per_page: int
    bookmarks: List[BookmarkResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        bookmarks: List[Bookmark],
        page: int,
        items_per_page: int,
    ) -> "BookmarkPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            bookmarks=[
                BookmarkResponse.from_domain(bookmark) for bookmark in bookmarks
            ],
        )


class CurriculumSocialInfoResponse(BaseModel):
    """커리큘럼 소셜 정보 응답"""

    curriculum_id: str
    like_count: int
    is_liked: bool
    is_bookmarked: bool
