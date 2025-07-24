import pytest
from datetime import datetime, timezone
from ulid import ULID

from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore


class InMemoryFeedbackRepo(IFeedbackRepository):
    def __init__(self):
        self._store: dict[tuple[ULID, int], list[Feedback]] = {}
        # summary_id → list of (curriculum_id, week)
        self._by_summary: dict[ULID, list[tuple[ULID, int]]] = {}

    def save(self, curriculum_id, week_number, feedback: Feedback) -> None:
        key = (curriculum_id, week_number.value)
        self._store.setdefault(key, []).append(feedback)
        self._by_summary.setdefault(feedback.id, []).append(key)

    def find_by_week(self, curriculum_id, week_number) -> list[Feedback]:
        return list(self._store.get((curriculum_id, week_number.value), []))

    def find_all(self, curriculum_id) -> list[Feedback]:
        result: list[Feedback] = []
        for (cid, _), lst in self._store.items():
            if cid == curriculum_id:
                result.extend(lst)
        return result

    def delete_by_summary(self, summary_id: ULID) -> None:
        if summary_id not in self._by_summary:
            raise KeyError(f"No feedback for summary {summary_id}")
        # 1) summary_id에 매핑된 주차 키들을 꺼냄
        keys = self._by_summary.pop(summary_id)
        # 2) 각 키에서 해당 feedback만 제거
        for key in keys:
            feedbacks = self._store.get(key, [])
            # 필터링: id가 summary_id와 일치하지 않는 것만 남김
            self._store[key] = [fb for fb in feedbacks if fb.id != summary_id]
            if not self._store[key]:
                del self._store[key]


def make_feedback(curriculum_id, week):
    now = datetime.now(timezone.utc)
    return Feedback(
        id=ULID(),
        comment=FeedbackComment("Great summary!"),
        score=FeedbackScore(8),
        created_at=now,
    )


@pytest.fixture
def sample_repo():
    return InMemoryFeedbackRepo()


@pytest.fixture
def sample_key():
    return ULID(), WeekNumber(1)


def test_save_and_find_by_week(sample_repo, sample_key):
    cid, wn = sample_key
    f1 = make_feedback(cid, wn)
    f2 = make_feedback(cid, wn)
    sample_repo.save(cid, wn, f1)
    sample_repo.save(cid, wn, f2)
    results = sample_repo.find_by_week(cid, wn)
    assert results == [f1, f2]


def test_find_all(sample_repo, sample_key):
    cid, wn = sample_key
    f1 = make_feedback(cid, wn)
    f2 = make_feedback(cid, wn)
    other_cid = ULID()
    f3 = make_feedback(other_cid, wn)
    sample_repo.save(cid, wn, f1)
    sample_repo.save(cid, wn, f2)
    sample_repo.save(other_cid, wn, f3)
    all_fb = sample_repo.find_all(cid)
    assert set(all_fb) == {f1, f2}


def test_delete_by_summary(sample_repo, sample_key):
    cid, wn = sample_key
    fb = make_feedback(cid, wn)
    sample_repo.save(cid, wn, fb)
    # ensure stored
    assert sample_repo.find_by_week(cid, wn) == [fb]
    # delete
    sample_repo.delete_by_summary(fb.id)
    # now empty
    assert sample_repo.find_by_week(cid, wn) == []


def test_delete_by_summary_missing_raises(sample_repo):
    with pytest.raises(KeyError):
        sample_repo.delete_by_summary(ULID())
