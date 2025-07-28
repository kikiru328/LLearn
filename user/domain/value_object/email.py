from typing import Any
from email_validator import validate_email, EmailNotValidError


class Email:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Email must be a string")

        self._value: str = raw.lower().strip()

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Email {self._value}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Email) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
