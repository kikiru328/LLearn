class FeedbackComment:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Feedback comment must be a string")

        cleaned = raw.strip()
        if not cleaned:
            raise ValueError("Feedback comment cannot be empty or whitespace only")

        self._value = raw.strip()

    @property
    def value(self) -> str:
        return self._value

    @property
    def length(self) -> int:
        return len(self._value)

    def __repr__(self) -> str:
        return f"<FeedbackComment length={len(self._value)}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeedbackComment) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
