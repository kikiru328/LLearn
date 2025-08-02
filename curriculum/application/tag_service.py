from datetime import datetime, timezone
from typing import List, Optional, Tuple
from ulid import ULID

from curriculum.application.exception import (
    CategoryNotFoundError,
    CurriculumNotFoundError,
    DuplicateCategoryError,
    TagNotFoundError,
)
from curriculum.domain.entity.category import Category
from curriculum.domain.entity.tag import Tag
from curriculum.domain.entity.curriculum_tag import CurriculumTag
from curriculum.domain.repository.category_repo import ICategoryRepository
from curriculum.domain.repository.tag_repo import ITagRepository
from curriculum.domain.repository.curriculum_tag_repo import (
    ICurriculumTagRepository,
    ICurriculumCategoryRepository,
)
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.category_name import CategoryName
from curriculum.domain.value_object.tag_name import TagName
from user.domain.value_object.role import RoleVO


class TagService:
    def __init__(
        self,
        category_repo: ICategoryRepository,
        tag_repo: ITagRepository,
        curriculum_tag_repo: ICurriculumTagRepository,
        curriculum_category_repo: ICurriculumCategoryRepository,
        curriculum_repo: ICurriculumRepository,
        ulid: ULID = ULID(),
    ) -> None:
        self.category_repo = category_repo
        self.tag_repo = tag_repo
        self.curriculum_tag_repo = curriculum_tag_repo
        self.curriculum_category_repo = curriculum_category_repo
        self.curriculum_repo = curriculum_repo
        self.ulid = ulid

    # ========================= CATEGORY 관련 메서드 =========================

    async def create_category(
        self,
        name: str,
        description: Optional[str],
        color: str,
        icon: Optional[str] = None,
        sort_order: int = 0,
    ) -> Category:
        """카테고리 생성 (관리자만)"""
        category_name = CategoryName(name)

        # 중복 확인
        if await self.category_repo.exists_by_name(category_name):
            raise DuplicateCategoryError(f"Category '{name}' already exists")

        now = datetime.now(timezone.utc)
        category = Category(
            id=self.ulid.generate(),
            name=category_name,
            description=description,
            color=color,
            icon=icon,
            sort_order=sort_order,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        await self.category_repo.create(category)
        return category

    async def get_categories(
        self,
        page: int = 1,
        items_per_page: int = 20,
        include_inactive: bool = False,
    ) -> Tuple[int, List[Category]]:
        """카테고리 목록 조회"""
        return await self.category_repo.find_all(
            page=page,
            items_per_page=items_per_page,
            include_inactive=include_inactive,
        )

    async def get_active_categories(self) -> List[Category]:
        """활성화된 카테고리 목록 조회"""
        return await self.category_repo.find_all_active()

    async def update_category(
        self,
        category_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        sort_order: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> Category:
        """카테고리 수정 (관리자만)"""
        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        # 이름 변경 시 중복 확인
        if name and name != category.name.value:
            new_name = CategoryName(name)
            if await self.category_repo.exists_by_name(new_name):
                raise DuplicateCategoryError(f"Category '{name}' already exists")
            category.name = new_name

        if description is not None:
            category.description = description
        if color:
            category.color = color
        if icon is not None:
            category.icon = icon
        if sort_order is not None:
            category.sort_order = sort_order
        if is_active is not None:
            category.is_active = is_active

        category.updated_at = datetime.now(timezone.utc)
        await self.category_repo.update(category)
        return category

    # ========================= TAG 관련 메서드 =========================

    async def create_tag(
        self,
        name: str,
        created_by: str,
    ) -> Tag:
        """태그 생성"""
        tag_name = TagName(name)

        # 기존 태그 확인
        existing_tag = await self.tag_repo.find_by_name(tag_name)
        if existing_tag:
            return existing_tag  # 이미 존재하면 기존 태그 반환

        now = datetime.now(timezone.utc)
        tag = Tag(
            id=self.ulid.generate(),
            name=tag_name,
            usage_count=0,
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )

        await self.tag_repo.create(tag)
        return tag

    async def get_popular_tags(
        self,
        limit: int = 20,
        min_usage: int = 1,
    ) -> List[Tag]:
        """인기 태그 조회"""
        return await self.tag_repo.find_popular_tags(
            limit=limit,
            min_usage=min_usage,
        )

    async def search_tags(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Tag]:
        """태그 검색 (자동완성용)"""
        return await self.tag_repo.search_by_name(query, limit)

    async def get_tags(
        self,
        page: int = 1,
        items_per_page: int = 20,
    ) -> Tuple[int, List[Tag]]:
        """모든 태그 조회"""
        return await self.tag_repo.find_all(page, items_per_page)

    # ========================= CURRICULUM-TAG 관련 메서드 =========================

    async def add_tags_to_curriculum(
        self,
        curriculum_id: str,
        tag_names: List[str],
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> List[Tag]:
        """커리큘럼에 태그 추가"""
        # 커리큘럼 존재 및 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 권한 확인
        if role != RoleVO.ADMIN and curriculum.owner_id != user_id:
            raise PermissionError("You can only add tags to your own curriculum")

        # 태그 이름들을 TagName VO로 변환
        tag_name_vos = TagName.from_list(tag_names)

        # 태그들을 찾거나 생성
        tags = await self.tag_repo.find_or_create_by_names(tag_name_vos, user_id)

        now = datetime.now(timezone.utc)
        added_tags = []

        for tag in tags:
            # 이미 연결되어 있는지 확인
            existing_connection = (
                await self.curriculum_tag_repo.find_by_curriculum_and_tag(
                    curriculum_id, tag.id
                )
            )

            if not existing_connection:
                # 새 연결 생성
                curriculum_tag = CurriculumTag(
                    id=self.ulid.generate(),
                    curriculum_id=curriculum_id,
                    tag_id=tag.id,
                    added_by=user_id,
                    created_at=now,
                )
                await self.curriculum_tag_repo.create(curriculum_tag)

                # 태그 사용횟수 증가
                await self.tag_repo.increment_usage_count(tag.id)
                added_tags.append(tag)

        return added_tags

    async def remove_tag_from_curriculum(
        self,
        curriculum_id: str,
        tag_name: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> None:
        """커리큘럼에서 태그 제거"""
        # 커리큘럼 존재 및 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 권한 확인
        if role != RoleVO.ADMIN and curriculum.owner_id != user_id:
            raise PermissionError("You can only remove tags from your own curriculum")

        # 태그 찾기
        tag = await self.tag_repo.find_by_name(TagName(tag_name))
        if not tag:
            raise TagNotFoundError(f"Tag '{tag_name}' not found")

        # 연결 삭제
        await self.curriculum_tag_repo.delete_by_curriculum_and_tag(
            curriculum_id, tag.id
        )

        # 태그 사용횟수 감소
        await self.tag_repo.decrement_usage_count(tag.id)

    async def get_curriculum_tags(self, curriculum_id: str) -> List[Tag]:
        """커리큘럼의 태그 목록 조회"""
        return await self.curriculum_tag_repo.find_tags_by_curriculum(curriculum_id)

    async def find_curriculums_by_tags(
        self,
        tag_names: List[str],
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[str]]:
        """태그로 커리큘럼 검색"""
        return await self.curriculum_tag_repo.find_curriculums_by_tag_names(
            tag_names, page, items_per_page
        )

    # ========================= CURRICULUM-CATEGORY 관련 메서드 =========================

    async def assign_category_to_curriculum(
        self,
        curriculum_id: str,
        category_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> Category:
        """커리큘럼에 카테고리 할당"""
        # 커리큘럼 존재 및 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 권한 확인
        if role != RoleVO.ADMIN and curriculum.owner_id != user_id:
            raise PermissionError("You can only assign category to your own curriculum")

        # 카테고리 존재 확인
        category = await self.category_repo.find_by_id(category_id)
        if not category or not category.is_active:
            raise CategoryNotFoundError(f"Active category {category_id} not found")

        # 기존 카테고리가 있으면 업데이트, 없으면 새로 생성
        await self.curriculum_category_repo.update_curriculum_category(
            curriculum_id, category_id, user_id
        )

        return category

    async def remove_category_from_curriculum(
        self,
        curriculum_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> None:
        """커리큘럼에서 카테고리 제거"""
        # 커리큘럼 존재 및 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 권한 확인
        if role != RoleVO.ADMIN and curriculum.owner_id != user_id:
            raise PermissionError(
                "You can only remove category from your own curriculum"
            )

        await self.curriculum_category_repo.delete_by_curriculum(curriculum_id)

    async def get_curriculum_category(self, curriculum_id: str) -> Optional[Category]:
        """커리큘럼의 카테고리 조회"""
        return await self.curriculum_category_repo.find_category_by_curriculum(
            curriculum_id
        )

    async def find_curriculums_by_category(
        self,
        category_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[str]]:
        """카테고리로 커리큘럼 검색"""
        return await self.curriculum_category_repo.find_curriculums_by_category(
            category_id, page, items_per_page
        )
