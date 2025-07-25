from typing import Any
from email_validator import validate_email, EmailNotValidError


class Email:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Email must be a string")

        try:
            # validate_email은 유효성 검사 + 정규화된 이메일 반환
            valid = validate_email(raw, check_deliverability=False)
            self._value = valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {str(e)}")

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Email {self._value}>"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other) if isinstance(other, Email) else False

    def __hash__(self) -> int:
        return hash(self._value)
