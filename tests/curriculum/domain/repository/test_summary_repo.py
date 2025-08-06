import pytest
from datetime import datetime, timezone
from ulid import ULID
from curriculum.domain.entity.summary import Summary
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.value_object.week_number import WeekNumber


class InMemorySummaryRepo(ISummaryRepository):
    def __init__(self):
        self._store: dict[ULID, Summary] = {}
        self._index: dict[tuple[ULID, int], list[ULID]] = {}

    def save(
        self,
        curriculum_id,
        week_number,
        summary: Summary,
    ) -> None:
        self._store[summary.id] = summary
        key = (curriculum_id, week_number.value)
        self._index.setdefault(key, []).append(summary.id)

    def find_by_week(self, curriculum_id, week_number):
        key = (curriculum_id, week_number.value)
        return [self._store[sid] for sid in self._index.get(key, [])]

    def delete(self, summary_id):
        # 1) 존재 확인
        if summary_id not in self._store:
            raise KeyError(f"Summary {summary_id} not found")
        # 2) 인덱스에서 제거
        self._store.pop(summary_id)
        for key, lst in list(self._index.items()):
            if summary_id in lst:
                lst.remove(summary_id)
                if not lst:
                    del self._index[key]


def test_summary_repo_save_and_find_by_week():
    repo = InMemorySummaryRepo()
    cid = ULID()
    wn = WeekNumber(1)
    s1 = Summary(
        id=ULID(),
        content=SummaryContent("a" * 300),
        submitted_at=datetime.now(timezone.utc),
    )
    s2 = Summary(
        id=ULID(),
        content=SummaryContent("b" * 300),
        submitted_at=datetime.now(timezone.utc),
    )

    repo.save(cid, wn, s1)
    repo.save(cid, wn, s2)
    results = repo.find_by_week(cid, wn)
    assert results == [s1, s2]


def test_summary_repo_delete():
    repo = InMemorySummaryRepo()
    cid = ULID()
    wn = WeekNumber(1)
    s = Summary(
        id=ULID(),
        content=SummaryContent("c" * 300),
        submitted_at=datetime.now(timezone.utc),
    )

    repo.save(cid, wn, s)
    assert repo.find_by_week(cid, wn) == [s]

    repo.delete(s.id)
    assert repo.find_by_week(cid, wn) == []
    # non-existent delete should KeyError
    with pytest.raises(KeyError):
        repo.delete(s.id)
