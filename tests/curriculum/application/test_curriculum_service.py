from datetime import datetime, timezone
import pytest
from ulid import ULID
from curriculum.application.curriculum_service import CurriculumService

from curriculum.application.exception import CurriculumNotFoundError
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.repository import curriculum_repo
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository


class InMemoryCurriculumRepo(ICurriculumRepository):
    def __init__(self):
        self._saved: dict[ULID, Curriculum] = {}

    async def save(self, curriculum: Curriculum):
        if curriculum.id in self._saved:
            raise ValueError("already exist curriculum")
        self._saved[curriculum.id] = curriculum

    async def find_by_id(self, id: ULID):
        return self._saved.get(id)

    async def find_curriculums(
        self,
        page: int = 1,
        items_per_page: int = 3,
    ):
        total_count: int = len(self._saved)
        curriculums = list(self._saved.values())[
            (page - 1) * items_per_page : page * items_per_page
        ]
        return total_count, curriculums

    async def update(self, curriculum: Curriculum):
        if curriculum.id not in self._saved:
            raise CurriculumNotFoundError(f"{id} not found")
        self._saved[curriculum.id] = curriculum

    async def delete(self, id: ULID):
        curriculum = self._saved.get(id)
        if curriculum is None:
            raise CurriculumNotFoundError(f"{id} not found")
        del self._saved[id]


pytestmark = pytest.mark.asyncio


async def test_create_curriculum_find_sucess():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock_curriculum = await curriculum_service.create_curriculum(
        title="Test Curriculum Title",
        week_schedules=[],
        created_at=now,
    )
    assert isinstance(mock_curriculum, Curriculum)
    assert await mock_repo.find_by_id(mock_curriculum.id) == mock_curriculum
    assert mock_curriculum.created_at == now
    assert mock_curriculum.title == "Test Curriculum Title"


async def test_find_curriculum_by_id_not_found():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    fake_id = ULID()
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_curriculum_by_id(fake_id)


async def test_find_curriculums():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )

    for i in range(5):
        await curriculum_service.create_curriculum(
            title=f"{i}_Test Curriculum",
            week_schedules=[],
        )

    total, page1 = await curriculum_service.get_curriculums(page=1, items_per_page=3)
    total, page2 = await curriculum_service.get_curriculums(page=2, items_per_page=2)

    assert total == 5
    assert len(page1) == 3
    assert len(page2) == 2


async def test_update_curriculum_title_sucess():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    now = datetime.now(timezone.utc)

    original = await curriculum_service.create_curriculum(
        title="Old Title", week_schedules=[], created_at=now
    )

    updated = await curriculum_service.update_curriculum_title(
        curriculum_id=original.id,
        title="New Title",
    )

    assert updated.id == original.id
    assert updated.title == "New Title"

    stored = await mock_repo.find_by_id(original.id)
    assert stored is not None and stored.title == "New Title"


async def test_update_curriculum_not_found():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.update_curriculum_title(
            ULID(),
            title="FAKE",
        )


async def test_delete_curriculum_sucess():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    now = datetime.now(timezone.utc)
    curriculum = await curriculum_service.create_curriculum(
        title="Title", week_schedules=[], created_at=now
    )

    await curriculum_service.delete_curriculum(curriculum.id)
    assert await mock_repo.find_by_id(curriculum.id) is None


async def test_delete_curriculum_not_found():
    mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=mock_repo,
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.delete_curriculum(ULID())
