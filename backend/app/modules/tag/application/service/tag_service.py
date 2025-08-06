from datetime import datetime, timezone
from typing import List, Optional
from ulid import ULID  # type: ignore

from app.modules.tag.application.dto.tag_dto import (
    CreateTagCommand,
    UpdateTagCommand,
    TagQuery,
    TagDTO,
    TagPageDTO,
)
from app.modules.tag.application.exception import (
    TagNotFoundError,
    DuplicateTagError,
    TagAccessDeniedError,
    InvalidTagNameError,
)
from app.modules.tag.domain.repository.tag_repo import ITagRepository
from app.modules.tag.domain.service.tag_domain_service import TagDomainService
from app.modules.user.domain.vo.role import RoleVO


class TagService:
    """태그 애플리케이션 서비스"""

    def __init__(
        self,
        tag_repo: ITagRepository,
        tag_domain_service: TagDomainService,
        ulid: ULID = ULID(),
    ) -> None:
        self.tag_repo = tag_repo
        self.tag_domain_service = tag_domain_service
        self.ulid = ulid

    async def create_tag(
        self,
        command: CreateTagCommand,
        created_at: Optional[datetime] = None,
    ) -> TagDTO:
        """태그 생성"""
        try:
            # 도메인 서비스를 통한 태그 생성
            tag = await self.tag_domain_service.create_tag(
                tag_id=self.ulid.generate(),
                name=command.name,
                created_by=command.created_by,
                created_at=created_at,
            )

            await self.tag_repo.save(tag)
            return TagDTO.from_domain(tag)

        except ValueError as e:
            raise InvalidTagNameError(str(e))

    async def get_tag_by_id(
        self,
        tag_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> TagDTO:
        """ID로 태그 조회"""
        tag = await self.tag_repo.find_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(f"Tag {tag_id} not found")

        return TagDTO.from_domain(tag)

    async def get_tag_by_name(
        self,
        name: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> Optional[TagDTO]:
        """이름으로 태그 조회"""
        try:
            tag_name = await self.tag_domain_service.validate_tag_creation(name)
            tag = await self.tag_repo.find_by_name(tag_name)
            if not tag:
                return None

            return TagDTO.from_domain(tag)

        except ValueError as e:
            raise InvalidTagNameError(str(e))

    async def get_popular_tags(
        self,
        limit: int = 20,
        min_usage: int = 1,
    ) -> List[TagDTO]:
        """인기 태그 목록 조회"""
        tags = await self.tag_repo.find_popular_tags(
            limit=limit,
            min_usage=min_usage,
        )
        return [TagDTO.from_domain(tag) for tag in tags]

    async def search_tags(
        self,
        query: str,
        limit: int = 10,
    ) -> List[TagDTO]:
        """태그 검색 (자동완성용)"""
        if not query.strip():
            return []

        tags = await self.tag_repo.search_by_name(query.strip(), limit)
        return [TagDTO.from_domain(tag) for tag in tags]

    async def get_tags(
        self,
        query: TagQuery,
    ) -> TagPageDTO:
        """태그 목록 조회"""
        if query.search_query:
            # 검색 모드
            tags = await self.tag_repo.search_by_name(
                query.search_query, query.items_per_page
            )
            total_count = len(tags)
            return TagPageDTO.from_domain(
                total_count=total_count,
                page=query.page,
                items_per_page=query.items_per_page,
                tags=tags,
            )
        else:
            # 전체 조회 모드
            total_count, tags = await self.tag_repo.find_all(
                page=query.page,
                items_per_page=query.items_per_page,
            )
            return TagPageDTO.from_domain(
                total_count=total_count,
                page=query.page,
                items_per_page=query.items_per_page,
                tags=tags,
            )

    async def update_tag(
        self,
        command: UpdateTagCommand,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> TagDTO:
        """태그 수정"""
        tag = await self.tag_repo.find_by_id(command.tag_id)
        if not tag:
            raise TagNotFoundError(f"Tag {command.tag_id} not found")

        # 권한 확인 (관리자 또는 태그 생성자만 수정 가능)
        if role != RoleVO.ADMIN and tag.created_by != user_id:
            raise TagAccessDeniedError("You can only modify your own tags")

        # 이름 변경
        if command.name and command.name.strip():
            try:
                new_name = await self.tag_domain_service.validate_tag_creation(
                    command.name
                )

                # 중복 확인 (자기 자신 제외)
                existing_tag = await self.tag_repo.find_by_name(new_name)
                if existing_tag and existing_tag.id != tag.id:
                    raise DuplicateTagError(f"Tag '{command.name}' already exists")

                tag.name = new_name
                tag.updated_at = datetime.now(timezone.utc)

            except ValueError as e:
                raise InvalidTagNameError(str(e))

        await self.tag_repo.update(tag)
        return TagDTO.from_domain(tag)

    async def delete_tag(
        self,
        tag_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> None:
        """태그 삭제"""
        tag = await self.tag_repo.find_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(f"Tag {tag_id} not found")

        # 권한 확인 (관리자만 삭제 가능)
        if role != RoleVO.ADMIN:
            raise TagAccessDeniedError("Only administrators can delete tags")

        await self.tag_repo.delete(tag_id)

    async def increment_tag_usage(self, tag_id: str) -> None:
        """태그 사용 횟수 증가"""
        await self.tag_repo.increment_usage_count(tag_id)

    async def decrement_tag_usage(self, tag_id: str) -> None:
        """태그 사용 횟수 감소"""
        await self.tag_repo.decrement_usage_count(tag_id)

    async def find_or_create_tags_by_names(
        self,
        tag_names: List[str],
        created_by: str,
    ) -> List[TagDTO]:
        """태그 이름 리스트로 태그들을 찾거나 생성"""
        try:
            tags = await self.tag_domain_service.find_or_create_tags_by_names(
                tag_names, created_by
            )
            return [TagDTO.from_domain(tag) for tag in tags]

        except ValueError as e:
            raise InvalidTagNameError(str(e))
