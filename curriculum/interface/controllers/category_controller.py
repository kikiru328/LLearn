from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role
from curriculum.application.tag_service import TagService
from curriculum.interface.schemas.tag_schema import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
    CategoryResponse,
    CategoryPageResponse,
    AssignCategoryRequest,
)
from DI.containers import Container


router = APIRouter(prefix="/categories", tags=["Categories"])


def assert_admin(current_user: CurrentUser) -> None:
    """관리자 권한 확인"""
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.post("/", response_model=CategoryResponse, status_code=201)
@inject
async def create_category(
    request: CreateCategoryRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
) -> CategoryResponse:
    """카테고리 생성 (관리자만)"""
    assert_admin(current_user)

    category = await tag_service.create_category(
        name=request.name,
        description=request.description,
        color=request.color,
        icon=request.icon,
        sort_order=request.sort_order,
    )
    return CategoryResponse.from_domain(category)


@router.get("/", response_model=CategoryPageResponse, status_code=200)
@inject
async def get_categories(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = Query(1, ge=1, description="페이지 번호"),
    items_per_page: int = Query(20, ge=1, le=50, description="페이지당 항목 수"),
    include_inactive: bool = Query(False, description="비활성화된 카테고리 포함 여부"),
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """카테고리 목록 조회"""
    total_count, categories = await tag_service.get_categories(
        page=page,
        items_per_page=items_per_page,
        include_inactive=include_inactive,
    )
    return CategoryPageResponse.from_domain(
        total_count, categories, page, items_per_page
    )


@router.get("/active", response_model=list[CategoryResponse], status_code=200)
@inject
async def get_active_categories(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """활성화된 카테고리 목록 조회"""
    categories = await tag_service.get_active_categories()
    return [CategoryResponse.from_domain(category) for category in categories]


@router.patch("/{category_id}", response_model=CategoryResponse, status_code=200)
@inject
async def update_category(
    category_id: str,
    request: UpdateCategoryRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
) -> CategoryResponse:
    """카테고리 수정 (관리자만)"""
    assert_admin(current_user)

    category = await tag_service.update_category(
        category_id=category_id,
        name=request.name,
        description=request.description,
        color=request.color,
        icon=request.icon,
        sort_order=request.sort_order,
        is_active=request.is_active,
    )
    return CategoryResponse.from_domain(category)


# 커리큘럼-카테고리 관련 엔드포인트
curriculum_categories_router = APIRouter(
    prefix="/curriculums", tags=["Curriculum Categories"]
)


@curriculum_categories_router.post(
    "/{curriculum_id}/category", response_model=CategoryResponse, status_code=201
)
@inject
async def assign_category_to_curriculum(
    curriculum_id: str,
    request: AssignCategoryRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
) -> CategoryResponse:
    """커리큘럼에 카테고리 할당"""
    category = await tag_service.assign_category_to_curriculum(
        curriculum_id=curriculum_id,
        category_id=request.category_id,
        user_id=current_user.id,
        role=current_user.role,
    )
    return CategoryResponse.from_domain(category)


@curriculum_categories_router.get(
    "/{curriculum_id}/category", response_model=CategoryResponse, status_code=200
)
@inject
async def get_curriculum_category(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """커리큘럼의 카테고리 조회"""
    category = await tag_service.get_curriculum_category(curriculum_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="카테고리가 할당되지 않았습니다.",
        )

    return CategoryResponse.from_domain(category)


@curriculum_categories_router.delete("/{curriculum_id}/category", status_code=204)
@inject
async def remove_category_from_curriculum(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    """커리큘럼에서 카테고리 제거"""
    await tag_service.remove_category_from_curriculum(
        curriculum_id=curriculum_id,
        user_id=current_user.id,
        role=current_user.role,
    )
