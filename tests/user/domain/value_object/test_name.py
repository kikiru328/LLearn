import pytest
from user.domain.value_object.name import Name


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Al", "Al"),
        ("Alice", "Alice"),
        ("Bob_1", "Bob_1"),
        ("AbcDefGh", "AbcDefGh"),
    ],
)
def test_valid_name_kept_as_is(raw, expected):
    assert str(Name(raw)) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "A",  # 1자
        "AbcDefGhi",  # 9자
        "John Doe",  # 공백
        "Alice-1",  # 허용되지 않은 특수문자
        "Bob!",  # 허용되지 않은 특수문자
        "   ",  # 공백만
    ],
)
def test_invalid_name_raises_value_error(raw):
    with pytest.raises(ValueError):
        Name(raw)


def test_name_equality_and_hash():
    assert Name("Alice") == Name("Alice")
    assert {Name("Bob_1")} == {Name("Bob_1")}
