# user/domain/value_object/email.py
import re
from typing import Any

_SIMPLE_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class Email:
    __slots__ = ("_value",)  # 객체 속성만 저장

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str) or not _SIMPLE_EMAIL_RE.fullmatch(raw):
            raise ValueError("Invalid email format")
        self._value = raw.lower()

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Email {self._value}>"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other) if isinstance(other, Email) else False

    def __hash__(self) -> int:  # 동일한 값 확인
        return hash(self._value)
