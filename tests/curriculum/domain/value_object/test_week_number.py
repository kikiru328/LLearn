import pytest
from curriculum.domain.value_object.week_number import WeekNumber


@pytest.mark.parametrize("invalid_week", [0, 25, -5, 100])
def test_week_number_out_of_range_raises(invalid_week):
    with pytest.raises(ValueError):
        WeekNumber(invalid_week)


def test_week_number_valid():
    w = WeekNumber(1)
    assert w.value == 1
    w = WeekNumber(24)
    assert w.value == 24
