class WeekNumber:
    __slots__ = ("_value",)

    def __init__(self, raw: int) -> None:
        if not isinstance(raw, int) or not (1 <= raw <= 24):
            raise ValueError(
                f"WeekNumber must be an integer between 1 and 24 (got {raw})"
            )
        self._value = raw

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, WeekNumber) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"<WeekNumber {self._value}>"
