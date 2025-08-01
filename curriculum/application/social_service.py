from datetime import datetime, timezone
from typing import List, Optional, Tuple
from ulid import ULID

from curriculum.application.exception import CurriculumNotFoundError
from curriculum.domain.entity.like import Like
from curriculum.domain.entity.bookmark import Bookmark
from curriculum.domain.repository.like_repo import ILikeRepository
from curriculum.domain.repository.bookmark_repo import IBookmarkRepository
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from user.domain.value_object.role import RoleVO


class SocialService:
    def __init__(
        self,
        like_repo: ILikeRepository,
        bookmark_repo: IBookmarkRepository,
        curriculum_repo: ICurriculumRepository,
        ulid: ULID = ULID(),
    ) -> None:
        self.like_repo: ILikeRepository = like_repo
        self.bookmark_repo: IBookmarkRepository = bookmark_repo
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.ulid: ULID = ulid

    # ========================= LIKE 관련 메서드 =========================

    async def toggle_like(
        self,
        user_id: str,
        curriculum_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> dict:
        """좋아요 토글 (좋아요 추가/제거)"""
        # 커리큘럼 존재 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 기존 좋아요 확인
        existing_like = await self.like_repo.find_by_user_and_curriculum(
            user_id=user_id, curriculum_id=curriculum_id
        )

        if existing_like:
            # 좋아요 취소
            await self.like_repo.delete_by_user_and_curriculum(
                user_id=user_id, curriculum_id=curriculum_id
            )
            is_liked = False
        else:
            # 좋아요 추가
            new_like = Like(
                id=self.ulid.generate(),
                user_id=user_id,
                curriculum_id=curriculum_id,
                created_at=datetime.now(timezone.utc),
            )
            await self.like_repo.create(new_like)
            is_liked = True

        # 현재 좋아요 수 조회
        like_count = await self.like_repo.count_by_curriculum(curriculum_id)

        return {
            "is_liked": is_liked,
            "like_count": like_count,
        }

    async def get_curriculum_likes(
        self,
        curriculum_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Like]]:
        """커리큘럼의 좋아요 목록 조회"""
        return await self.like_repo.find_by_curriculum(
            curriculum_id=curriculum_id,
            page=page,
            items_per_page=items_per_page,
        )

    async def get_user_likes(
        self,
        user_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Like]]:
        """사용자가 좋아요한 목록 조회"""
        return await self.like_repo.find_by_user(
            user_id=user_id,
            page=page,
            items_per_page=items_per_page,
        )

    async def is_liked_by_user(
        self,
        user_id: str,
        curriculum_id: str,
    ) -> bool:
        """사용자가 해당 커리큘럼을 좋아요했는지 확인"""
        like = await self.like_repo.find_by_user_and_curriculum(
            user_id=user_id, curriculum_id=curriculum_id
        )
        return like is not None

    # ========================= BOOKMARK 관련 메서드 =========================

    async def toggle_bookmark(
        self,
        user_id: str,
        curriculum_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> dict:
        """북마크 토글 (북마크 추가/제거)"""
        # 커리큘럼 존재 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 기존 북마크 확인
        existing_bookmark = await self.bookmark_repo.find_by_user_and_curriculum(
            user_id=user_id, curriculum_id=curriculum_id
        )

        if existing_bookmark:
            # 북마크 취소
            await self.bookmark_repo.delete_by_user_and_curriculum(
                user_id=user_id, curriculum_id=curriculum_id
            )
            is_bookmarked = False
        else:
            # 북마크 추가
            new_bookmark = Bookmark(
                id=self.ulid.generate(),
                user_id=user_id,
                curriculum_id=curriculum_id,
                created_at=datetime.now(timezone.utc),
            )
            await self.bookmark_repo.create(new_bookmark)
            is_bookmarked = True

        return {
            "is_bookmarked": is_bookmarked,
        }

    async def get_user_bookmarks(
        self,
        user_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Bookmark]]:
        """사용자의 북마크 목록 조회"""
        return await self.bookmark_repo.find_by_user(
            user_id=user_id,
            page=page,
            items_per_page=items_per_page,
        )

    async def is_bookmarked_by_user(
        self,
        user_id: str,
        curriculum_id: str,
    ) -> bool:
        """사용자가 해당 커리큘럼을 북마크했는지 확인"""
        bookmark = await self.bookmark_repo.find_by_user_and_curriculum(
            user_id=user_id, curriculum_id=curriculum_id
        )
        return bookmark is not None
