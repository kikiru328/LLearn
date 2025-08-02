from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from curriculum.domain.entity.category import Category
from curriculum.domain.entity.tag import Tag


# ========================= CATEGORY 스키마 =========================


class CreateCategoryRequest(BaseModel):
    """카테고리 생성 요청"""

    name: str = Field(min_length=2, max_length=30, description="카테고리 이름")
    description: Optional[str] = Field(
        None, max_length=500, description="카테고리 설명"
    )
    color: str = Field(
        min_length=7, max_length=7, description="헥스 색상 코드 (예: #FF5733)"
    )
    icon: Optional[str] = Field(None, max_length=50, description="아이콘 이름")
    sort_order: int = Field(default=0, description="정렬 순서")


class UpdateCategoryRequest(BaseModel):
    """카테고리 수정 요청"""

    name: Optional[str] = Field(
        None, min_length=2, max_length=30, description="카테고리 이름"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="카테고리 설명"
    )
    color: Optional[str] = Field(
        None, min_length=7, max_length=7, description="헥스 색상 코드"
    )
    icon: Optional[str] = Field(None, max_length=50, description="아이콘 이름")
    sort_order: Optional[int] = Field(None, description="정렬 순서")
    is_active: Optional[bool] = Field(None, description="활성화 여부")


class CategoryResponse(BaseModel):
    """카테고리 응답"""

    id: str
    name: str
    description: Optional[str]
    color: str
    icon: Optional[str]
    sort_order: int
    is_active: bool
    curriculum_count: int = 0  # 해당 카테고리를 사용하는 커리큘럼 수
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(
        cls, category: Category, curriculum_count: int = 0
    ) -> "CategoryResponse":
        return cls(
            id=category.id,
            name=category.name.value,
            description=category.description,
            color=category.color,
            icon=category.icon,
            sort_order=category.sort_order,
            is_active=category.is_active,
            curriculum_count=curriculum_count,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )


class CategoryPageResponse(BaseModel):
    """카테고리 목록 페이지 응답"""

    total_count: int
    page: int
    items_per_page: int
    categories: List[CategoryResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        categories: List[Category],
        page: int,
        items_per_page: int,
        curriculum_counts: List[int] = None,
    ) -> "CategoryPageResponse":
        if curriculum_counts is None:
            curriculum_counts = [0] * len(categories)

        category_responses = [
            CategoryResponse.from_domain(category, count)
            for category, count in zip(categories, curriculum_counts)
        ]

        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            categories=category_responses,
        )


# ========================= TAG 스키마 =========================


class CreateTagRequest(BaseModel):
    """태그 생성 요청"""

    name: str = Field(min_length=1, max_length=20, description="태그 이름")


class AddTagsRequest(BaseModel):
    """커리큘럼에 태그 추가 요청"""

    tag_names: List[str] = Field(
        min_items=1, max_items=10, description="추가할 태그 이름들"
    )


class RemoveTagRequest(BaseModel):
    """커리큘럼에서 태그 제거 요청"""

    tag_name: str = Field(min_length=1, max_length=20, description="제거할 태그 이름")


class TagResponse(BaseModel):
    """태그 응답"""

    id: str
    name: str
    usage_count: int
    is_popular: bool = False  # 인기 태그 여부
    created_by: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, tag: Tag, popular_threshold: int = 10) -> "TagResponse":
        return cls(
            id=tag.id,
            name=tag.name.value,
            usage_count=tag.usage_count,
            is_popular=tag.is_popular(popular_threshold),
            created_by=tag.created_by,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )


class TagPageResponse(BaseModel):
    """태그 목록 페이지 응답"""

    total_count: int
    page: int
    items_per_page: int
    tags: List[TagResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        tags: List[Tag],
        page: int,
        items_per_page: int,
    ) -> "TagPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            tags=[TagResponse.from_domain(tag) for tag in tags],
        )


# ========================= CURRICULUM-CATEGORY/TAG 스키마 =========================


class AssignCategoryRequest(BaseModel):
    """커리큘럼에 카테고리 할당 요청"""

    category_id: str = Field(description="할당할 카테고리 ID")


class CurriculumTagsResponse(BaseModel):
    """커리큘럼 태그 목록 응답"""

    curriculum_id: str
    tags: List[TagResponse]
    category: Optional[CategoryResponse]

    @classmethod
    def from_domain(
        cls, curriculum_id: str, tags: List[Tag], category: Optional[Category] = None
    ) -> "CurriculumTagsResponse":
        return cls(
            curriculum_id=curriculum_id,
            tags=[TagResponse.from_domain(tag) for tag in tags],
            category=CategoryResponse.from_domain(category) if category else None,
        )


class TagSearchResponse(BaseModel):
    """태그 검색 응답 (자동완성용)"""

    suggestions: List[TagResponse]

    @classmethod
    def from_domain(cls, tags: List[Tag]) -> "TagSearchResponse":
        return cls(suggestions=[TagResponse.from_domain(tag) for tag in tags])
