from dataclasses import dataclass
from datetime import datetime
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore


@dataclass
class Feedback:
    comment: FeedbackComment
    score: FeedbackScore
    created_at: datetime

    def __post_init__(self):
        if not isinstance(self.comment, FeedbackComment):
            raise TypeError(
                f"comment must be a FeedbackComment instance, got {type(self.comment).__name__}"
            )
        if not isinstance(self.score, FeedbackScore):
            raise TypeError(
                f"score must be a FeedbackScore instance, got {type(self.score).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be a datetime instance, got {type(self.created_at).__name__}"
            )
