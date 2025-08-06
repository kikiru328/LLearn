from datetime import datetime
from typing import List, Optional
from ulid import ULID  # type: ignore

from app.modules.tag.application.dto.tag_dto import (
    CreateCategoryCommand,
    UpdateCategoryCommand,
    CategoryQuery,
    CategoryDTO,
    CategoryPageDTO,
)
from app.modules.tag.application.exception import (
    CategoryNotFoundError,
    DuplicateCategoryError,
    CategoryAccessDeniedError,
    InvalidCategoryNameError,
)
from app.modules.tag.domain.repository.category_repo import ICategoryRepository
from app.modules.tag.domain.service.tag_domain_service import TagDomainService
from app.modules.user.domain.vo.role import RoleVO


class CategoryService:
    """카테고리 애플리케이션 서비스"""

    def __init__(
        self,
        category_repo: ICategoryRepository,
        tag_domain_service: TagDomainService,
        ulid: ULID = ULID(),
    ) -> None:
        self.category_repo = category_repo
        self.tag_domain_service = tag_domain_service
        self.ulid = ulid

    async def create_category(
        self,
        command: CreateCategoryCommand,
        user_id: str,
        role: RoleVO = RoleVO.USER,
        created_at: Optional[datetime] = None,
    ) -> CategoryDTO:
        """카테고리 생성 (관리자만)"""
        if role != RoleVO.ADMIN:
            raise CategoryAccessDeniedError("Only administrators can create categories")

        try:
            # 도메인 서비스를 통한 유효성 검증
            await self.tag_domain_service.validate_category_creation(command.name)

            # 카테고리 생성
            category = await self.tag_domain_service.create_category(
                category_id=self.ulid.generate(),
                name=command.name,
                description=command.description,
                color=command.color,
                icon=command.icon,
                sort_order=command.sort_order,
                created_at=created_at,
            )

            await self.category_repo.save(category)
            return CategoryDTO.from_domain(category)

        except ValueError as e:
            if "already exists" in str(e):
                raise DuplicateCategoryError(str(e))
            raise InvalidCategoryNameError(str(e))

    async def get_category_by_id(
        self,
        category_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> CategoryDTO:
        """ID로 카테고리 조회"""
        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        return CategoryDTO.from_domain(category)

    async def get_active_categories(self) -> List[CategoryDTO]:
        """활성화된 카테고리 목록 조회"""
        categories = await self.category_repo.find_all_active()
        return [CategoryDTO.from_domain(category) for category in categories]

    async def get_categories(
        self,
        query: CategoryQuery,
    ) -> CategoryPageDTO:
        """카테고리 목록 조회"""
        total_count, categories = await self.category_repo.find_all(
            page=query.page,
            items_per_page=query.items_per_page,
            include_inactive=query.include_inactive,
        )

        return CategoryPageDTO.from_domain(
            total_count=total_count,
            page=query.page,
            items_per_page=query.items_per_page,
            categories=categories,
        )

    async def update_category(
        self,
        command: UpdateCategoryCommand,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> CategoryDTO:
        """카테고리 수정 (관리자만)"""
        if role != RoleVO.ADMIN:
            raise CategoryAccessDeniedError("Only administrators can modify categories")

        category = await self.category_repo.find_by_id(command.category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {command.category_id} not found")

        try:
            # 이름 변경
            if command.name:
                await self.tag_domain_service.validate_category_creation(
                    command.name, exclude_category_id=category.id
                )
                category.change_name(
                    await self.tag_domain_service.validate_category_creation(
                        command.name, category.id
                    )
                )

            # 기타 속성 변경
            if command.description is not None:
                category.change_description(command.description)

            if command.color:
                category.change_color(command.color)

            if command.icon is not None:
                category.icon = command.icon
                category._touch_updated_at()

            if command.sort_order is not None:
                category.change_sort_order(command.sort_order)

            if command.is_active is not None:
                if command.is_active:
                    category.activate()
                else:
                    category.deactivate()

            await self.category_repo.update(category)
            return CategoryDTO.from_domain(category)

        except ValueError as e:
            if "already exists" in str(e):
                raise DuplicateCategoryError(str(e))
            raise InvalidCategoryNameError(str(e))

    async def delete_category(
        self,
        category_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> None:
        """카테고리 삭제 (관리자만)"""
        if role != RoleVO.ADMIN:
            raise CategoryAccessDeniedError("Only administrators can delete categories")

        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        # TODO: 사용 중인 카테고리인지 확인
        # curriculum_count = await self.curriculum_category_repo.count_by_category(category_id)
        # if curriculum_count > 0:
        #     raise CategoryInUseError(f"Category is used by {curriculum_count} curriculums")

        await self.category_repo.delete(category_id)

    async def activate_category(
        self,
        category_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> CategoryDTO:
        """카테고리 활성화 (관리자만)"""
        if role != RoleVO.ADMIN:
            raise CategoryAccessDeniedError(
                "Only administrators can activate categories"
            )

        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        category.activate()
        await self.category_repo.update(category)
        return CategoryDTO.from_domain(category)

    async def deactivate_category(
        self,
        category_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> CategoryDTO:
        """카테고리 비활성화 (관리자만)"""
        if role != RoleVO.ADMIN:
            raise CategoryAccessDeniedError(
                "Only administrators can deactivate categories"
            )

        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        category.deactivate()
        await self.category_repo.update(category)
        return CategoryDTO.from_domain(category)
