from dataclasses import dataclass
from datetime import datetime
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from ulid import ULID


@dataclass
class Feedback:
    id: ULID
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
        if not isinstance(self.id, ULID):
            raise TypeError(f"id must be a ULID instance, got {type(self.id).__name__}")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Feedback) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
