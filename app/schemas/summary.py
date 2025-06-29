from uuid import UUID

from pydantic import BaseModel, Field

class CreateSummaryRequest(BaseModel):
    week_topic_id: UUID = Field(
        ...,
        description="주차 ID"
    )
    content: str = Field(
        ...,
        min_length=50,
        max_length=5000,
        description="주차별 요약문"
    )

    is_public: bool = Field(
        default=False,
        description="공개 여부"
    )
