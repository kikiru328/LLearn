class SummaryContent:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("Summary content must not be empty")
        if len(raw) < 300:
            raise ValueError("Summary content must be at least 300 characters")
        if len(raw) > 10_000:
            raise ValueError("Summary content must be at most 10,000 characters")
        self._value = raw.strip()

    @property
    def value(self) -> str:
        return self._value
