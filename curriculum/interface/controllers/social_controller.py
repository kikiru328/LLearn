from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user
from curriculum.application.social_service import SocialService
from curriculum.interface.schemas.social_schema import (
    LikeToggleResponse,
    BookmarkToggleResponse,
    LikePageResponse,
    BookmarkPageResponse,
    CurriculumSocialInfoResponse,
)
from DI.containers import Container


router = APIRouter(prefix="/curriculums", tags=["Social"])


@router.post(
    "/{curriculum_id}/like", response_model=LikeToggleResponse, status_code=200
)
@inject
async def toggle_like(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    social_service: SocialService = Depends(Provide[Container.social_service]),
) -> LikeToggleResponse:
    """커리큘럼 좋아요 토글"""
    result = await social_service.toggle_like(
        user_id=current_user.id,
        curriculum_id=curriculum_id,
        role=current_user.role,
    )
    return LikeToggleResponse(**result)


@router.post(
    "/{curriculum_id}/bookmark", response_model=BookmarkToggleResponse, status_code=200
)
@inject
async def toggle_bookmark(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    social_service: SocialService = Depends(Provide[Container.social_service]),
) -> BookmarkToggleResponse:
    """커리큘럼 북마크 토글"""
    result = await social_service.toggle_bookmark(
        user_id=current_user.id,
        curriculum_id=curriculum_id,
        role=current_user.role,
    )
    return BookmarkToggleResponse(**result)


@router.get("/{curriculum_id}/likes", response_model=LikePageResponse, status_code=200)
@inject
async def get_curriculum_likes(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    social_service: SocialService = Depends(Provide[Container.social_service]),
):
    """커리큘럼의 좋아요 목록 조회"""
    total_count, likes = await social_service.get_curriculum_likes(
        curriculum_id=curriculum_id,
        page=page,
        items_per_page=items_per_page,
    )
    return LikePageResponse.from_domain(total_count, likes, page, items_per_page)


@router.get(
    "/{curriculum_id}/social-info",
    response_model=CurriculumSocialInfoResponse,
    status_code=200,
)
@inject
async def get_curriculum_social_info(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    social_service: SocialService = Depends(Provide[Container.social_service]),
):
    """커리큘럼의 소셜 정보 조회 (좋아요수, 사용자의 좋아요/북마크 여부)"""
    # 좋아요 수 조회
    total_likes, _ = await social_service.get_curriculum_likes(
        curriculum_id=curriculum_id, page=1, items_per_page=1
    )

    # 사용자의 좋아요/북마크 여부 확인
    is_liked = await social_service.is_liked_by_user(
        user_id=current_user.id, curriculum_id=curriculum_id
    )
    is_bookmarked = await social_service.is_bookmarked_by_user(
        user_id=current_user.id, curriculum_id=curriculum_id
    )

    return CurriculumSocialInfoResponse(
        curriculum_id=curriculum_id,
        like_count=total_likes,
        is_liked=is_liked,
        is_bookmarked=is_bookmarked,
    )


# 사용자 관련 소셜 기능
user_social_router = APIRouter(prefix="/users/me", tags=["User Social"])


@user_social_router.get("/likes", response_model=LikePageResponse, status_code=200)
@inject
async def get_my_likes(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    social_service: SocialService = Depends(Provide[Container.social_service]),
):
    """내가 좋아요한 커리큘럼 목록"""
    total_count, likes = await social_service.get_user_likes(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )
    return LikePageResponse.from_domain(total_count, likes, page, items_per_page)


@user_social_router.get(
    "/bookmarks", response_model=BookmarkPageResponse, status_code=200
)
@inject
async def get_my_bookmarks(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    social_service: SocialService = Depends(Provide[Container.social_service]),
):
    """내 북마크 목록"""
    total_count, bookmarks = await social_service.get_user_bookmarks(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )
    return BookmarkPageResponse.from_domain(
        total_count, bookmarks, page, items_per_page
    )
