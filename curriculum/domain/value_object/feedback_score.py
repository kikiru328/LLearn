class FeedbackScore:
    __slots__ = ("_value",)

    def __init__(self, raw: int) -> None:
        if not isinstance(raw, int) or not (1 <= raw <= 10):
            raise ValueError("Feedback score must be an integer between 1 and 10")
        self._value = raw

    @property
    def value(self) -> int:
        return self._value
