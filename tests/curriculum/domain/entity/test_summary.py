import pytest
from datetime import datetime, timezone
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.entity.summary import Summary


def test_summary_entity_accepts_valid_summary_content_and_datetime():
    valid_text = "x" * 300
    summary_content = SummaryContent(valid_text)
    submission_time = datetime.now(timezone.utc)

    summary_entity = Summary(content=summary_content, submitted_at=submission_time)

    assert summary_entity.content == summary_content
    assert summary_entity.submitted_at == submission_time


@pytest.mark.parametrize(
    "bad_content,bad_time",
    [
        ("not a VO", datetime.now(timezone.utc)),  # content wrong type
        (SummaryContent("y" * 300), "not a datetime"),  # submitted_at wrong type
    ],
)
def test_summary_entity_rejects_wrong_types(bad_content, bad_time):
    with pytest.raises(TypeError):
        Summary(content=bad_content, submitted_at=bad_time)
