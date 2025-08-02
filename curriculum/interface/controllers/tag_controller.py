from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user
from curriculum.application.tag_service import TagService
from curriculum.interface.schemas.tag_schema import (
    CreateTagRequest,
    AddTagsRequest,
    RemoveTagRequest,
    TagResponse,
    TagPageResponse,
    CurriculumTagsResponse,
    TagSearchResponse,
)
from DI.containers import Container


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagResponse, status_code=201)
@inject
async def create_tag(
    request: CreateTagRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
) -> TagResponse:
    """태그 생성"""
    tag = await tag_service.create_tag(
        name=request.name,
        created_by=current_user.id,
    )
    return TagResponse.from_domain(tag)


@router.get("/popular", response_model=list[TagResponse], status_code=200)
@inject
async def get_popular_tags(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    limit: int = Query(20, ge=1, le=50, description="조회할 태그 수"),
    min_usage: int = Query(1, ge=1, description="최소 사용 횟수"),
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """인기 태그 목록 조회"""
    tags = await tag_service.get_popular_tags(limit=limit, min_usage=min_usage)
    return [TagResponse.from_domain(tag) for tag in tags]


@router.get("/search", response_model=TagSearchResponse, status_code=200)
@inject
async def search_tags(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    q: str = Query(..., min_length=1, description="검색 쿼리"),
    limit: int = Query(10, ge=1, le=20, description="조회할 태그 수"),
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """태그 검색 (자동완성용)"""
    tags = await tag_service.search_tags(query=q, limit=limit)
    return TagSearchResponse.from_domain(tags)


@router.get("/", response_model=TagPageResponse, status_code=200)
@inject
async def get_tags(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = Query(1, ge=1, description="페이지 번호"),
    items_per_page: int = Query(20, ge=1, le=50, description="페이지당 항목 수"),
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """모든 태그 목록 조회"""
    total_count, tags = await tag_service.get_tags(
        page=page,
        items_per_page=items_per_page,
    )
    return TagPageResponse.from_domain(total_count, tags, page, items_per_page)


# 커리큘럼-태그 관련 엔드포인트
curriculum_tags_router = APIRouter(prefix="/curriculums", tags=["Curriculum Tags"])


@curriculum_tags_router.post(
    "/{curriculum_id}/tags", response_model=list[TagResponse], status_code=201
)
@inject
async def add_tags_to_curriculum(
    curriculum_id: str,
    request: AddTagsRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """커리큘럼에 태그 추가"""
    tags = await tag_service.add_tags_to_curriculum(
        curriculum_id=curriculum_id,
        tag_names=request.tag_names,
        user_id=current_user.id,
        role=current_user.role,
    )
    return [TagResponse.from_domain(tag) for tag in tags]


@curriculum_tags_router.get(
    "/{curriculum_id}/tags", response_model=CurriculumTagsResponse, status_code=200
)
@inject
async def get_curriculum_tags(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """커리큘럼의 태그 및 카테고리 조회"""
    tags = await tag_service.get_curriculum_tags(curriculum_id)
    category = await tag_service.get_curriculum_category(curriculum_id)

    return CurriculumTagsResponse.from_domain(
        curriculum_id=curriculum_id,
        tags=tags,
        category=category,
    )


@curriculum_tags_router.delete("/{curriculum_id}/tags", status_code=204)
@inject
async def remove_tag_from_curriculum(
    curriculum_id: str,
    request: RemoveTagRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """커리큘럼에서 태그 제거"""
    await tag_service.remove_tag_from_curriculum(
        curriculum_id=curriculum_id,
        tag_name=request.tag_name,
        user_id=current_user.id,
        role=current_user.role,
    )
