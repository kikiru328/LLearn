import pytest
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.topics import Topics
from curriculum.domain.entity.week_schedule import WeekSchedule


def test_week_schedule_creates_with_valid_value_objects():
    week_number_vo = WeekNumber(2)
    topics_vo = Topics(["Intro", "Setup"])
    week_schedule = WeekSchedule(week_number=week_number_vo, topics=topics_vo)

    assert week_schedule.week_number == week_number_vo
    assert week_schedule.topics == topics_vo


def test_week_schedule_rejects_raw_types():
    # WeekNumber, Topics VO가 아닌 값으로는 생성 불가
    with pytest.raises(TypeError):
        WeekSchedule(week_number=2, topics=["A", "B"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        WeekSchedule(week_number=WeekNumber(1), topics="not a list")  # type: ignore[arg-type]
