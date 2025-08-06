import pytest
from ulid import ULID
from datetime import datetime, timezone
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.topics import Topics
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.entity.curriculum import Curriculum


def test_curriculum_creation_with_valid_value_objects():
    curriculum_id = ULID()
    now = datetime.now(timezone.utc)
    week1 = WeekSchedule(
        week_number=WeekNumber(1), topics=Topics(["python basic", "python functions"])
    )
    curriculum = Curriculum(
        id=curriculum_id,
        title=Title("My Curriculum"),
        created_at=now,
        updated_at=now,
        week_schedules=[week1],
    )

    assert curriculum.id == curriculum_id
    assert curriculum.title == "My Curriculum"
    assert curriculum.created_at == now
    assert curriculum.updated_at == now
    assert curriculum.week_schedules == [week1]


@pytest.mark.parametrize(
    "bad_id,bad_title,bad_created,bad_updated,bad_weeks",
    [
        (  # ULID ERROR
            "not a ULID",
            "Title",
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
            [],
        ),
        (  # Title Error
            ULID(),
            "",
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
            [],
        ),
        (  # datetime error (created_at)
            ULID(),
            "Title",
            "not datetime",
            datetime.now(timezone.utc),
            [],
        ),
        (  # updated_at error
            ULID(),
            "Title",
            datetime.now(timezone.utc),
            "not datetime",
            [],
        ),
        (  # list schedules error
            ULID(),
            "Title",
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
            "not a list",
        ),
    ],
)
def test_curriculum_rejects_invalid_types(
    bad_id, bad_title, bad_created, bad_updated, bad_weeks
):

    with pytest.raises((TypeError, ValueError)):
        Curriculum(
            id=bad_id,
            title=Title(bad_title),
            created_at=bad_created,
            updated_at=bad_updated,
            week_schedules=bad_weeks,
        )
