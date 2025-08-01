from dataclasses import dataclass
from datetime import datetime
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore


@dataclass
class Feedback:
    id: str
    summary_id: str
    comment: FeedbackComment
    score: FeedbackScore
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise TypeError(f"id must be str, got {type(self.id).__name__}")
        if not isinstance(self.summary_id, str):
            raise TypeError(
                f"summary_id must be str, got {type(self.summary_id).__name__}"
            )
        if not isinstance(self.comment, FeedbackComment):
            raise TypeError(
                f"comment must be FeedbackComment, got {type(self.comment).__name__}"
            )
        if not isinstance(self.score, FeedbackScore):
            raise TypeError(
                f"score must be FeedbackScore, got {type(self.score).__name__}"
            )
        if not isinstance(self.created_at, datetime):
            raise TypeError(
                f"created_at must be datetime, got {type(self.created_at).__name__}"
            )
