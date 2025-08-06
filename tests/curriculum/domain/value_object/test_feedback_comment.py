import pytest

from curriculum.domain.value_object.feedback_comment import FeedbackComment


@pytest.mark.parametrize("raw", ["정말 좋은 요약이였습니다"])
def test_feedback_comment_valid(raw):
    assert FeedbackComment(raw).value == raw


@pytest.mark.parametrize("raw", ["", " "])
def test_feedback_comment_invalid(raw):
    with pytest.raises(ValueError):
        FeedbackComment(raw)
