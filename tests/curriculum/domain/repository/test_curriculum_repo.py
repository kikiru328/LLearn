from datetime import datetime, timezone
import pytest
from ulid import ULID

from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.topics import Topics
from curriculum.domain.value_object.week_number import WeekNumber


class InMemoryCurriculumRepository(ICurriculumRepository):
    def __init__(self) -> None:
        self._store: dict[ULID, Curriculum] = {}

    def save(self, curriculum: Curriculum) -> None:
        if curriculum.id in self._store:
            raise ValueError("duplicate curriculum")
        self._store[curriculum.id] = curriculum

    def find_by_id(self, id: ULID) -> Curriculum | None:
        return self._store.get(id)

    def find_curriculums(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> tuple[int, list[Curriculum]]:

        total_count: int = len(self._store)
        return total_count, list(self._store.values())

    def update(self, curriculum: Curriculum):
        if curriculum.id not in self._store:
            return None
        self._store[curriculum.id] = curriculum

    def delete(self, id):
        del self._store[id]


def make_sample_curriculum(weeks_count: int = 1) -> Curriculum:
    now = datetime.now(timezone.utc)
    week_schedules = [
        WeekSchedule(week_number=WeekNumber(i + 1), topics=Topics([f"Topic {i+1}"]))
        for i in range(weeks_count)
    ]
    return Curriculum(
        id=ULID(),
        title=Title("Sample Curriculum"),
        created_at=now,
        updated_at=now,
        week_schedules=week_schedules,
    )


def test_save_and_find_by_id():
    repo = InMemoryCurriculumRepository()
    curriculum = make_sample_curriculum(2)

    repo.save(curriculum)
    found = repo.find_by_id(curriculum.id)

    assert found == curriculum


def test_save_duplicate_raises_value_error():
    repo = InMemoryCurriculumRepository()
    curriculum = make_sample_curriculum()

    repo.save(curriculum)
    with pytest.raises(ValueError):
        repo.save(curriculum)


def test_find_all_returns_all_saved_curricula():
    repo = InMemoryCurriculumRepository()
    first = make_sample_curriculum()
    second = make_sample_curriculum()

    repo.save(first)
    repo.save(second)

    all_curricula = repo._store.values()
    assert first in all_curricula and second in all_curricula
    assert len(all_curricula) == 2


def test_find_all_curriculums_paging():
    repo = InMemoryCurriculumRepository()
    # 15개 저장
    for i in range(15):
        curriculum = make_sample_curriculum()
        repo.save(curriculum)
    total, page1 = repo.find_curriculums(page=1, items_per_page=10)
    assert total == 15
    assert len(page1) == 15


def test_update_existing_curriculum():
    repo = InMemoryCurriculumRepository()
    curriculum = make_sample_curriculum()
    repo.save(curriculum)

    curriculum.title = Title("Updated Title")
    repo.update(curriculum)

    found = repo.find_by_id(curriculum.id)
    assert found is not None
    assert found.title == "Updated Title"


def test_update_nonexistent_noop():
    repo = InMemoryCurriculumRepository()
    curriculum = make_sample_curriculum()

    # 저장안함

    assert repo.update(curriculum) is None
    assert repo.find_by_id(curriculum.id) is None


def test_delete_existent_curriculum():
    repo = InMemoryCurriculumRepository()
    curriculum = make_sample_curriculum()
    repo.save(curriculum)

    repo.delete(curriculum.id)
    assert repo.find_by_id(curriculum.id) is None


def test_delete_nonexistent_curriculum():
    repo = InMemoryCurriculumRepository()
    with pytest.raises(KeyError):
        repo.delete(ULID("nonexistent-id"))
