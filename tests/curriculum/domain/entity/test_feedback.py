from datetime import datetime, timezone
import pytest

from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore


def test_feeback_entity_valid_value():
    comment_vo = FeedbackComment("Great work on your summary!")
    score_vo = FeedbackScore(8)
    creation_time = datetime.now(timezone.utc)

    feedback_entity = Feedback(
        comment=comment_vo, score=score_vo, created_at=creation_time
    )

    assert feedback_entity.comment == comment_vo
    assert feedback_entity.score == score_vo
    assert feedback_entity.created_at == creation_time


@pytest.mark.parametrize(
    "bad_comment,bad_score,bad_time",
    [
        ("not a VO", FeedbackScore(5), datetime.now(timezone.utc)),
        (FeedbackComment("Nice!"), 5, datetime.now(timezone.utc)),
        (FeedbackComment("Nice!"), FeedbackScore(5), "not a datetime"),
    ],
)
def test_feedback_entity_rejects_wrong_types(bad_comment, bad_score, bad_time):
    with pytest.raises(TypeError):
        Feedback(comment=bad_comment, score=bad_score, created_at=bad_time)
