from dataclasses import dataclass
from datetime import datetime
from curriculum.domain.value_object.summary_content import SummaryContent


@dataclass
class Summary:
    content: SummaryContent
    submitted_at: datetime

    def __post_init__(self):  # 입력받는 시점에 확인
        if not isinstance(self.content, SummaryContent):
            raise TypeError(
                f"content must be a SummaryContent instance, got {type(self.content).__name__}"
            )
        if not isinstance(self.submitted_at, datetime):
            raise TypeError(
                f"submitted_at must be a datetime instance, got {type(self.submitted_at).__name__}"
            )
