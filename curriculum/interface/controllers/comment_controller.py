from typing import Annotated
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user
from curriculum.application.comment_service import CommentService
from curriculum.interface.schemas.comment_schema import (
    CreateCommentRequest,
    UpdateCommentRequest,
    CommentResponse,
    CommentPageResponse,
    CurriculumCommentStatsResponse,
)
from DI.containers import Container


router = APIRouter(prefix="/curriculums", tags=["Comments"])


@router.post(
    "/{curriculum_id}/comments", response_model=CommentResponse, status_code=201
)
@inject
async def create_comment(
    curriculum_id: str,
    request: CreateCommentRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
) -> CommentResponse:
    """댓글 작성"""
    comment = await comment_service.create_comment(
        user_id=current_user.id,
        curriculum_id=curriculum_id,
        content=request.content,
        parent_comment_id=request.parent_comment_id,
        role=current_user.role,
    )

    # 대댓글 수 조회 (최상위 댓글인 경우에만)
    reply_count = 0
    if not comment.parent_comment_id:
        reply_count = await comment_service.get_comment_reply_count(comment.id)

    return CommentResponse.from_domain(comment, reply_count)


@router.get(
    "/{curriculum_id}/comments", response_model=CommentPageResponse, status_code=200
)
@inject
async def get_curriculum_comments(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
):
    """커리큘럼의 댓글 목록 조회 (최상위 댓글만)"""
    total_count, comments = await comment_service.get_curriculum_comments(
        curriculum_id=curriculum_id,
        user_id=current_user.id,
        role=current_user.role,
        page=page,
        items_per_page=items_per_page,
    )

    # 각 댓글의 대댓글 수 조회
    reply_counts = []
    for comment in comments:
        reply_count = await comment_service.get_comment_reply_count(comment.id)
        reply_counts.append(reply_count)

    return CommentPageResponse.from_domain(
        total_count=total_count,
        comments=comments,
        page=page,
        items_per_page=items_per_page,
        reply_counts=reply_counts,
    )


@router.get(
    "/{curriculum_id}/comments/stats",
    response_model=CurriculumCommentStatsResponse,
    status_code=200,
)
@inject
async def get_curriculum_comment_stats(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
):
    """커리큘럼의 댓글 통계"""
    total_comment_count = await comment_service.get_curriculum_comment_count(
        curriculum_id
    )

    return CurriculumCommentStatsResponse(
        curriculum_id=curriculum_id,
        total_comment_count=total_comment_count,
    )


@router.get(
    "/comments/{parent_comment_id}/replies",
    response_model=CommentPageResponse,
    status_code=200,
)
@inject
async def get_comment_replies(
    parent_comment_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
):
    """댓글의 대댓글 목록 조회"""
    total_count, replies = await comment_service.get_comment_replies(
        parent_comment_id=parent_comment_id,
        user_id=current_user.id,
        role=current_user.role,
        page=page,
        items_per_page=items_per_page,
    )

    return CommentPageResponse.from_domain(
        total_count=total_count,
        comments=replies,
        page=page,
        items_per_page=items_per_page,
    )


@router.put("/comments/{comment_id}", response_model=CommentResponse, status_code=200)
@inject
async def update_comment(
    comment_id: str,
    request: UpdateCommentRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
) -> CommentResponse:
    """댓글 수정"""
    comment = await comment_service.update_comment(
        comment_id=comment_id,
        user_id=current_user.id,
        content=request.content,
        role=current_user.role,
    )

    # 대댓글 수 조회 (최상위 댓글인 경우에만)
    reply_count = 0
    if not comment.parent_comment_id:
        reply_count = await comment_service.get_comment_reply_count(comment.id)

    return CommentResponse.from_domain(comment, reply_count)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_comment(
    comment_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
):
    """댓글 삭제 (소프트 삭제)"""
    await comment_service.delete_comment(
        comment_id=comment_id,
        user_id=current_user.id,
        role=current_user.role,
    )


# 사용자 관련 댓글 기능
user_comment_router = APIRouter(prefix="/users/me", tags=["User Comments"])


@user_comment_router.get(
    "/comments", response_model=CommentPageResponse, status_code=200
)
@inject
async def get_my_comments(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
):
    """내가 작성한 댓글 목록"""
    total_count, comments = await comment_service.get_user_comments(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )

    return CommentPageResponse.from_domain(
        total_count=total_count,
        comments=comments,
        page=page,
        items_per_page=items_per_page,
    )
