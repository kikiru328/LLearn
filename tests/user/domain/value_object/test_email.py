import pytest
from user.domain.value_object.email import Email


@pytest.mark.parametrize(
    "raw",
    [
        "User@gamil.com",
        "foo.bar-baz@sub.domain.com",
    ],
)
def test_valid_email_normalize_to_lowercase(raw) -> None:
    email = Email(raw)
    assert str(email) == raw.lower()


@pytest.mark.parametrize(
    "raw",
    [
        "invalid@",
        "foo@.com",
        "bar.com",
        "",
    ],
)
def test_invalid_email_raises_value_error(raw) -> None:
    with pytest.raises(ValueError):
        Email(raw)


def test_email_equlity():
    assert Email("A@b.com") == Email("a@B.com")
    assert {Email("x@y.com")} == {Email("X@Y.COM")}


@pytest.mark.parametrize("raw", ["test@ example.com", "foo\n@bar.com"])
def test_email_rejects_whitespace(raw):
    with pytest.raises(ValueError):
        Email(raw)
