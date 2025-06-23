from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.curriculum import Curriculum
from domain.repositories.curriculum_repository import CurriculumRepository
from infrastructure.database.models.curriculum_model import CurriculumModel


class CurriculumRepositoryImpl(CurriculumRepository):
    """Curriculum Repository SQLAlchemy Implementation"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, curriculum: Curriculum) -> Curriculum:
        curriculum_model = CurriculumModel(
            id=str(curriculum.id),
            user_id=str(curriculum.user_id),
            title=curriculum.title,
            goal=curriculum.goal,
            duration_weeks=curriculum.duration_weeks,
            is_public=curriculum.is_public,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at
        )

        self.session.add(curriculum_model)
        await self.session.commit()
        await self.session.refresh(curriculum_model)

        return self._model_to_entity(curriculum_model)

    async def find_by_id(self, curriculum_id: UUID) -> Optional[Curriculum]:
        stmt = select(CurriculumModel).where(CurriculumModel.id == str(curriculum_id))
        result = await self.session.execute(stmt)
        curriculum_model = result.scalar_one_or_none()
        if curriculum_model is None:
            return None
        return self._model_to_entity(curriculum_model)

    async def find_by_user_id(self, user_id: UUID) -> List[Curriculum]:
        stmt = select(CurriculumModel).where(CurriculumModel.user_id == str(user_id))
        result = await self.session.execute(stmt)
        curriculum_models = result.scalars().all()
        return [self._model_to_entity(model) for model in curriculum_models]

    async def find_public_curriculums(self) -> List[Curriculum]:
        stmt = select(CurriculumModel).where(CurriculumModel.is_public == True)
        result = await self.session.execute(stmt)
        curriculum_models = result.scalars().all()
        return [self._model_to_entity(model) for model in curriculum_models]

    async def find_all(self) -> List[Curriculum]:
        stmt = select(CurriculumModel)
        result = await self.session.execute(stmt)
        curriculum_models = result.scalars().all()
        return [self._model_to_entity(model) for model in curriculum_models]

    async def delete(self, curriculum_id: UUID) -> bool:
        stmt = select(CurriculumModel).where(CurriculumModel.id == str(curriculum_id))
        result = await self.session.execute(stmt)
        curriculum_model = result.scalar_one_or_none()

        if curriculum_model is None:
            return False

        await self.session.delete(curriculum_model)
        await self.session.commit()
        return True

    def _model_to_entity(self, curriculum_model: CurriculumModel) -> Curriculum:
        return Curriculum(
            id=UUID(curriculum_model.id),
            user_id=UUID(curriculum_model.user_id),
            title=curriculum_model.title,
            goal=curriculum_model.goal,
            duration_weeks=curriculum_model.duration_weeks,
            is_public=curriculum_model.is_public,
            created_at=curriculum_model.created_at,
            updated_at=curriculum_model.updated_at
        )



