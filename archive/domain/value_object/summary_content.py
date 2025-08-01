class SummaryContent:
    __slots__ = ("_value",)

    MIN_LENGTH = 300
    MAX_LENGTH = 10_000

    def __init__(self, raw: str) -> None:

        cleaned = raw.strip()
        if not cleaned:
            raise ValueError("Summary content cannot be empty or whitespace only")

        if len(cleaned) < self.MIN_LENGTH:
            raise ValueError(
                f"Summary content must be at least {self.MIN_LENGTH} characters, got {len(cleaned)}"
            )

        if len(cleaned) > self.MAX_LENGTH:
            raise ValueError(
                f"Summary content must be at most {self.MAX_LENGTH} characters, got {len(cleaned)}"
            )

        self._value = cleaned

    @property
    def value(self) -> str:
        return self._value

    @property
    def length(self) -> int:
        return len(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<SummaryContent length={len(self._value)}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SummaryContent) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
