class FeedbackScore:
    __slots__ = ("_value",)

    MIN_SCORE = 1
    MAX_SCORE = 10

    def __init__(self, raw: int) -> None:
        if not isinstance(raw, int):
            raise ValueError(
                f"Feedback score must be an integer, got {type(raw).__name__}"
            )

        if not (self.MIN_SCORE <= raw <= self.MAX_SCORE):
            raise ValueError(
                f"Feedback score must be between {self.MIN_SCORE} and {self.MAX_SCORE}, got {raw}"
            )

        self._value = raw

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return f"{self._value}/10"

    def __repr__(self) -> str:
        return f"<FeedbackScore {self._value}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FeedbackScore) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
