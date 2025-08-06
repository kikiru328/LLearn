import pytest

from curriculum.domain.value_object.summary_content import SummaryContent


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("a" * 500, "a" * 500),
        ("b" * 300, "b" * 300),
        ("c" * 10_000, "c" * 10_000),
        (" " * 5 + ("b" * 300) + " " * 3, "b" * 300),
    ],
)
def test_valid_summary_content(raw, expected):
    assert SummaryContent(raw).value == expected


@pytest.mark.parametrize("raw", ["a" * 299, "b" * 10_001])
def test_invalid_length(raw):
    with pytest.raises(ValueError):
        SummaryContent(raw)
