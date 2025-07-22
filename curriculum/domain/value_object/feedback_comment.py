class FeedbackComment:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not raw or not raw.strip():
            raise ValueError("Feedback comment must not be empty")
        self._value = raw.strip()

    @property
    def value(self) -> str:
        return self._value
