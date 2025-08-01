from typing import Any


class Title:
    __slots__ = ("_value",)

    MIN_LENGTH = 1
    MAX_LENGTH = 50

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Title Must in String")

        cleaned = raw.strip()

        if not cleaned:
            raise ValueError("Title은 공백으로만 이루어질 수 없습니다.")

        if not (self.MIN_LENGTH <= len(cleaned) <= self.MAX_LENGTH):
            raise ValueError(
                f"Title length must be between {self.MIN_LENGTH} and {self.MAX_LENGTH} characters, got {len(cleaned)}"
            )

        self._value = cleaned

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Title {self._value}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Title) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    @property
    def value(self) -> str:
        return self._value
