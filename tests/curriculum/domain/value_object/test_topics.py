import pytest
from typing import Any
from curriculum.domain.value_object.topics import Topics


@pytest.mark.parametrize(
    "invalid_input",
    [
        [],  # 빈 리스트
        ["", "Valid Topic"],  # 빈 문자열 포함
        ["   ", "Another Topic"],  # 공백만 있는 문자열 포함
        ["Good", 123],  # 문자열이 아닌 항목 포함
        [None, "Also Valid"],  # None 포함
    ],
)
def test_topics_rejects_invalid_inputs(invalid_input: Any):
    with pytest.raises(ValueError):
        Topics(invalid_input)


def test_topics_trims_whitespace_and_accepts_valid_list():
    raw_topics = ["  Topic One  ", "Topic Two"]
    topics_value_object = Topics(raw_topics)

    # 내부에는 스트립된 값이 저장되어야 함
    assert topics_value_object.items == ["Topic One", "Topic Two"]
