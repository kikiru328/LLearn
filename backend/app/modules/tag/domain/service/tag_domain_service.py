from datetime import datetime, timezone
from typing import List, Optional

from app.modules.tag.domain.entity.category import Category
from app.modules.tag.domain.entity.tag import Tag
from app.modules.tag.domain.repository.category_repo import ICategoryRepository
from app.modules.tag.domain.repository.tag_repo import ITagRepository
from app.modules.tag.domain.vo.category_name import CategoryName
from app.modules.tag.domain.vo.tag_name import TagName


class TagDomainService:
    """Tag 도메인 서비스"""

    def __init__(
        self,
        tag_repo: ITagRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.tag_repo = tag_repo
        self.category_repo = category_repo

    async def create_tag(
        self,
        tag_id: str,
        name: str,
        created_by: str,
        created_at: Optional[datetime] = None,
    ) -> Tag:
        """태그 생성"""
        now = created_at or datetime.now(timezone.utc)
        tag_name = TagName(name)

        # 중복 확인
        if await self.tag_repo.exists_by_name(tag_name):
            existing_tag = await self.tag_repo.find_by_name(tag_name)
            if existing_tag:
                return existing_tag

        tag = Tag(
            id=tag_id,
            name=tag_name,
            usage_count=0,
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )

        return tag

    async def create_category(
        self,
        category_id: str,
        name: str,
        description: Optional[str],
        color: str,
        icon: Optional[str] = None,
        sort_order: int = 0,
        created_at: Optional[datetime] = None,
    ) -> Category:
        """카테고리 생성"""
        now = created_at or datetime.now(timezone.utc)
        category_name = CategoryName(name)

        category = Category(
            id=category_id,
            name=category_name,
            description=description,
            color=color,
            icon=icon,
            sort_order=sort_order,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return category

    async def is_tag_name_unique(self, name: TagName) -> bool:
        """태그 이름 유일성 확인"""
        return not await self.tag_repo.exists_by_name(name)

    async def is_category_name_unique(self, name: CategoryName) -> bool:
        """카테고리 이름 유일성 확인"""
        return not await self.category_repo.exists_by_name(name)

    async def validate_tag_creation(self, name: str) -> TagName:
        """태그 생성 유효성 검증"""
        tag_name = TagName(name)

        # 중복 확인은 하지 않음 (중복 시 기존 태그 반환)
        return tag_name

    async def validate_category_creation(
        self, name: str, exclude_category_id: Optional[str] = None
    ) -> CategoryName:
        """카테고리 생성 유효성 검증"""
        category_name = CategoryName(name)

        # 중복 확인
        existing_category = await self.category_repo.find_by_name(category_name)
        if existing_category and existing_category.id != exclude_category_id:
            raise ValueError(f"Category '{name}' already exists")

        return category_name

    async def find_or_create_tags_by_names(
        self, tag_names: List[str], created_by: str
    ) -> List[Tag]:
        """태그 이름 리스트로 태그들을 찾거나 생성"""
        tag_name_vos = TagName.from_list(tag_names)
        return await self.tag_repo.find_or_create_by_names(tag_name_vos, created_by)
