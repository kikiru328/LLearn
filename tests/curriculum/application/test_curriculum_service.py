from datetime import datetime, timezone
import pytest
from ulid import ULID
from curriculum.application.curriculum_service import CurriculumService

from curriculum.application.exception import (
    CurriculumNotFoundError,
    WeekScheduleNotFoundError,
)
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.entity.summary import Summary
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.value_object.week_number import WeekNumber


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


class InMemorySummaryRepo(ISummaryRepository):
    def __init__(self):
        self.saved = []

    async def save(self, cid, wn, summary):
        self.saved.append((cid, wn, summary))

    async def find_by_week(self, cid, wn):
        return [s for c, w, s in self.saved if c == cid and w == wn]

    async def delete(self, summary_id):
        self.saved = [(c, w, s) for (c, w, s) in self.saved if s.id != summary_id]


class InMemoryFeedbackRepo(IFeedbackRepository):
    def __init__(self):
        # (curriculum_id, week_number, summary_id, feedback)
        self.saved: list[tuple[ULID, WeekNumber, ULID, Feedback]] = []

    async def save(
        self,
        curriculum_id: ULID,
        week_number: WeekNumber,
        summary_id: ULID,
        feedback: Feedback,
    ) -> None:
        self.saved.append((curriculum_id, week_number, summary_id, feedback))

    async def find_by_week(
        self,
        curriculum_id: ULID,
        week_number: WeekNumber,
    ) -> list[Feedback]:
        return [
            fb
            for (c, w, sid, fb) in self.saved
            if c == curriculum_id and w == week_number
        ]

    async def find_all(
        self,
        curriculum_id: ULID,
    ) -> list[Feedback]:
        return [fb for (c, w, sid, fb) in self.saved if c == curriculum_id]

    async def delete_by_summary(self, summary_id: ULID) -> None:
        self.saved = [
            (c, w, sid, fb) for (c, w, sid, fb) in self.saved if sid != summary_id
        ]


pytestmark = pytest.mark.asyncio


# --------------------------
# Curriculum Test: aggregate root
# --------------------------


async def test_create_curriculum_find_sucess():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mock_curriculum = await curriculum_service.create_curriculum(
        title="Test Curriculum Title",
        week_schedules=[],
        created_at=now,
    )
    assert isinstance(mock_curriculum, Curriculum)
    assert await curriculum_mock_repo.find_by_id(mock_curriculum.id) == mock_curriculum
    assert mock_curriculum.created_at == now
    assert mock_curriculum.title == "Test Curriculum Title"


async def test_find_curriculum_by_id_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    fake_id = ULID()
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_curriculum_by_id(fake_id)


async def test_find_curriculums():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
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
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
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

    stored = await curriculum_mock_repo.find_by_id(original.id)
    assert stored is not None and stored.title == "New Title"


async def test_update_curriculum_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.update_curriculum_title(
            ULID(),
            title="FAKE",
        )


async def test_delete_curriculum_sucess():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    now = datetime.now(timezone.utc)
    curriculum = await curriculum_service.create_curriculum(
        title="Title", week_schedules=[], created_at=now
    )

    await curriculum_service.delete_curriculum(curriculum.id)
    assert await curriculum_mock_repo.find_by_id(curriculum.id) is None


async def test_delete_curriculum_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.delete_curriculum(ULID())


# --------------------------
# Week Schedule Test: sub domain (root: curriculum)
# --------------------------


async def test_add_week_schedule_success():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    # create curriculum
    curriculum = await curriculum_service.create_curriculum(
        title="Add Week Test",
        week_schedules=[],
    )

    # add new week schedules
    new_schedule = await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
        topics=["Topic A", "Topic B"],
    )

    # validation
    assert isinstance(new_schedule, WeekSchedule)
    assert new_schedule.week_number.value == 1
    assert new_schedule.topics.items == ["Topic A", "Topic B"]

    # check stored
    stored = await curriculum_mock_repo.find_by_id(curriculum.id)
    assert stored is not None
    assert any(ws.week_number.value == 1 for ws in stored.week_schedules)


async def test_add_week_schedule_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # 존재하지 않는 ID로 호출하면 NotFoundError
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.add_week_schedule(
            curriculum_id=ULID(),
            week_number=1,
            topics=["X"],
        )


async def test_get_week_schedule_success():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # create
    curriculum = await curriculum_service.create_curriculum(
        title="Get Week Test",
        week_schedules=[],
    )

    # add week_schedule
    await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=2,
        topics=["A", "B"],
    )

    # get week schedule
    schedule = await curriculum_service.get_week_schedule(
        curriculum_id=curriculum.id, week_number=2
    )

    assert isinstance(schedule, WeekSchedule)
    assert schedule.week_number.value == 2
    assert schedule.topics.items == ["A", "B"]


async def test_get_week_schedule_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_week_schedule(
            curriculum_id=ULID(),
            week_number=1,
        )


async def test_get_list_week_schedules_success():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # 커리큘럼 생성 + 두 개 주차 추가
    curriculum = await curriculum_service.create_curriculum(
        title="List Weeks Test",
        week_schedules=[],
    )
    await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
        topics=["T1"],
    )

    await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=2,
        topics=["T2"],
    )

    schedules = await curriculum_service.get_list_week_schedules(
        curriculum_id=curriculum.id
    )

    assert len(schedules) == 2
    assert all(isinstance(week_schedule, WeekSchedule) for week_schedule in schedules)


async def test_get_list_week_schedules_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_list_week_schedules(curriculum_id=ULID())


async def test_update_week_schedule_success():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # 커리큘럼 생성 + 1주차 추가
    curriculum = await curriculum_service.create_curriculum(
        title="Update Week Test",
        week_schedules=[],
    )
    await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
        topics=["Old A", "Old B"],
    )

    # 주차 스케줄 수정
    updated_schedule = await curriculum_service.update_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
        topics=["New X", "New Y"],
    )

    # 반환된 엔티티 확인
    assert isinstance(updated_schedule, WeekSchedule)
    assert updated_schedule.topics.items == ["New X", "New Y"]

    # 저장소 반영 확인
    stored = await curriculum_mock_repo.find_by_id(curriculum.id)
    assert any(
        ws.week_number.value == 1 and ws.topics.items == ["New X", "New Y"]
        for ws in stored.week_schedules
    )


async def test_update_week_schedule_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # curriculum이 없거나, 해당 주차가 없으면
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.update_week_schedule(
            curriculum_id=ULID(),
            week_number=1,
            topics=["X"],
        )

    # 커리큘럼은 있지만 2주차가 없을 때도 에러
    curriculum = await curriculum_service.create_curriculum(
        title="No Week2",
        week_schedules=[],
    )
    with pytest.raises(WeekScheduleNotFoundError):
        await curriculum_service.update_week_schedule(
            curriculum_id=curriculum.id,
            week_number=2,
            topics=["X"],
        )


async def test_delete_week_schedule_success():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    curriculum = await curriculum_service.create_curriculum(
        title="Delete Week Test",
        week_schedules=[],
    )
    await curriculum_service.add_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
        topics=["A", "B"],
    )

    await curriculum_service.delete_week_schedule(
        curriculum_id=curriculum.id,
        week_number=1,
    )

    stored = await curriculum_mock_repo.find_by_id(curriculum.id)
    assert all(ws.week_number.value != 1 for ws in stored.week_schedules)


async def test_delete_week_schedule_not_found():
    curriculum_mock_repo = InMemoryCurriculumRepo()
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    # no curriculum
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.delete_week_schedule(
            curriculum_id=ULID(),
            week_number=1,
        )

    # yes but no week
    curriculum = await curriculum_service.create_curriculum(
        title="No Such Week",
        week_schedules=[],
    )

    with pytest.raises(WeekScheduleNotFoundError):
        await curriculum_service.delete_week_schedule(
            curriculum_id=curriculum.id,
            week_number=2,
        )


# --------------------------
# Summary Test: sub domain (root: curriculum)
# --------------------------


async def test_submit_summary_success():
    summary_mock_repo = InMemorySummaryRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    curriculum = await curriculum_service.create_curriculum(
        title="SumTest",
        week_schedules=[],
    )

    # content
    content_vo = SummaryContent("x" * 500)
    summary = await curriculum_service.submit_summary(
        curriculum_id=curriculum.id,
        week_number=1,
        content=content_vo,
    )

    assert isinstance(summary, Summary)
    stored = await summary_mock_repo.find_by_week(
        curriculum.id,
        WeekNumber(1),
    )
    assert stored and stored[0] == summary


async def test_submit_summary_not_found():
    summary_mock_repo = InMemorySummaryRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )

    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.submit_summary(
            curriculum_id=ULID(),
            week_number=1,
            content=SummaryContent("x" * 300),
        )


async def test_get_summaries_by_week_success():
    summary_mock_repo = InMemorySummaryRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    curriculum = await curriculum_service.create_curriculum(
        title="Summary Week Test",
        week_schedules=[],
    )
    content1 = SummaryContent("a" * 400)
    content2 = SummaryContent("b" * 500)
    await curriculum_service.submit_summary(
        curriculum.id,
        week_number=1,
        content=content1,
    )
    await curriculum_service.submit_summary(
        curriculum.id,
        week_number=1,
        content=content2,
    )

    results = await curriculum_service.get_summaries_by_week(
        curriculum_id=curriculum.id,
        week_number=1,
    )
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(s, Summary) for s in results)


async def test_get_summaries_by_week_empty():
    summary_mock_repo = InMemorySummaryRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    curriculum = await curriculum_service.create_curriculum(
        title="Empty Summary Test",
        week_schedules=[],
    )

    results = await curriculum_service.get_summaries_by_week(
        curriculum_id=curriculum.id,
        week_number=2,
    )
    assert results == []


async def test_get_summaries_by_week_not_found():
    summary_mock_repo = InMemorySummaryRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_service = CurriculumService(
        curriculum_repo=curriculum_mock_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_mock_repo,
    )
    fake_id = ULID()
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_summaries_by_week(
            curriculum_id=fake_id,
            week_number=1,
        )


async def test_delete_summary_cascades_feedback():
    summary_mock_repo = InMemorySummaryRepo()
    feedback_repo = InMemoryFeedbackRepo()
    curriculum_repo = InMemoryCurriculumRepo()

    service = CurriculumService(
        curriculum_repo=curriculum_repo,
        summary_repo=summary_mock_repo,
        feedback_repo=feedback_repo,
    )

    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    # 1) 커리큘럼 생성 및 요약 제출
    curriculum = await service.create_curriculum("Test", [], created_at=now)
    content = SummaryContent("x" * 300)
    summary = await service.submit_summary(
        curriculum.id, week_number=1, content=content, submitted_at=now
    )

    # 2) 피드백 생성
    feedback = await service.provide_feedback(
        curriculum_id=curriculum.id,
        week_number=1,
        summary_id=summary.id,
        comment=FeedbackComment("잘했어요"),
        score=FeedbackScore(9),
    )

    # 3) 삭제 실행
    await service.delete_summary(summary_id=summary.id)

    # 4) 요약과 연관 피드백이 모두 제거됐는지 확인
    assert summary not in await summary_mock_repo.find_by_week(
        curriculum.id, WeekNumber(1)
    )
    assert feedback not in await feedback_repo.find_all(curriculum.id)


# --------------------------
# Feedback Test: sub domain (root: curriculum)
# --------------------------


async def test_get_feedbacks_by_week_success():
    # 준비
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_mock_repo, summary_mock_repo, feedback_mock_repo
    )

    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    curriculum = await curriculum_service.create_curriculum("Cur", [], created_at=now)
    summary = await curriculum_service.submit_summary(
        curriculum.id, 1, SummaryContent("x" * 300), submitted_at=now
    )
    fb1 = await curriculum_service.provide_feedback(
        curriculum.id, 1, summary.id, FeedbackComment("A"), FeedbackScore(5)
    )
    fb2 = await curriculum_service.provide_feedback(
        curriculum.id, 1, summary.id, FeedbackComment("B"), FeedbackScore(7)
    )

    # 실행
    results = await curriculum_service.get_feedbacks_by_week(curriculum.id, 1)

    # 검증
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(f, Feedback) for f in results)
    assert fb1 in results and fb2 in results


@pytest.mark.asyncio
async def test_get_feedbacks_by_week_empty():
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_mock_repo, summary_mock_repo, feedback_mock_repo
    )

    curriculum = await curriculum_service.create_curriculum(
        "Cur", [], created_at=datetime.now(timezone.utc)
    )

    results = await curriculum_service.get_feedbacks_by_week(curriculum.id, 2)
    assert results == []


@pytest.mark.asyncio
async def test_get_feedbacks_by_week_not_found_curriculum():
    curriculum_service = CurriculumService(
        InMemoryCurriculumRepo(), InMemorySummaryRepo(), InMemoryFeedbackRepo()
    )
    with pytest.raises(CurriculumNotFoundError):
        await curriculum_service.get_feedbacks_by_week(ULID(), 1)


@pytest.mark.asyncio
async def test_get_all_feedbacks_success():
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_mock_repo, summary_mock_repo, feedback_mock_repo
    )

    curriculum = await curriculum_service.create_curriculum(
        "C", [], created_at=datetime.now(timezone.utc)
    )
    summary = await curriculum_service.submit_summary(
        curriculum.id,
        1,
        SummaryContent("x" * 300),
        submitted_at=datetime.now(timezone.utc),
    )
    fb = await curriculum_service.provide_feedback(
        curriculum.id, 1, summary.id, FeedbackComment("OK"), FeedbackScore(8)
    )

    results = await curriculum_service.get_all_feedbacks(curriculum.id)
    assert results == [fb]


@pytest.mark.asyncio
async def test_delete_feedbacks_by_summary():
    summary_mock_repo = InMemorySummaryRepo()
    feedback_mock_repo = InMemoryFeedbackRepo()
    curriculum_mock_repo = InMemoryCurriculumRepo()
    curriculum_service = CurriculumService(
        curriculum_mock_repo, summary_mock_repo, feedback_mock_repo
    )

    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    curriculum = await curriculum_service.create_curriculum("C", [], created_at=now)
    summary = await curriculum_service.submit_summary(
        curriculum.id, 1, SummaryContent("x" * 300), submitted_at=now
    )
    await curriculum_service.provide_feedback(
        curriculum.id, 1, summary.id, FeedbackComment("OK"), FeedbackScore(8)
    )

    # 삭제
    await curriculum_service.delete_feedbacks_by_summary(summary.id)

    # 검증: 주차별, 전체 조회 모두 비어야 함
    assert await curriculum_service.get_feedbacks_by_week(curriculum.id, 1) == []
    assert await curriculum_service.get_all_feedbacks(curriculum.id) == []
