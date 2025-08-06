import pytest
from curriculum.domain.value_object.title import Title


@pytest.mark.parametrize("raw", ["커리큘럼"])
def test_title_valid(raw):
    assert Title(raw).value == raw


@pytest.mark.parametrize(
    "raw",
    [
        "길" * 100,
        "",
        "    ",
    ],
)
def test_title_invalid(raw):
    with pytest.raises(ValueError):
        Title(raw)
