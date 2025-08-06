import pytest

from curriculum.domain.value_object.feedback_score import FeedbackScore


@pytest.mark.parametrize("raw", [1, 5, 9])
def test_valid_feedback_score_range(raw):
    assert FeedbackScore(raw).value == raw


@pytest.mark.parametrize("raw", [0, -1, 11, 100, "5", None])
def test_invalid_feedback_score_vo(raw):
    with pytest.raises(ValueError):
        FeedbackScore(raw)
