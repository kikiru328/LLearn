from typing import List, Any


class Topics:
    __slots__ = ("_items",)

    def __init__(self, raw: List[Any]) -> None:

        if not isinstance(raw, list):
            raise ValueError("Topics Must be list")

        if len(raw) == 0:
            raise ValueError("Topics cannot be emtpy")

        # 3. 각 아이템 검증 및 정리
        cleaned_items = []
        for i, item in enumerate(raw):
            if not isinstance(item, str):
                raise ValueError(
                    f"Topic at index {i} must be a string, got {type(item).__name__}"
                )

            cleaned = item.strip()
            if not cleaned:
                raise ValueError(
                    f"Topic at index {i} cannot be empty or whitespace only"
                )

            cleaned_items.append(cleaned)

        self._items = cleaned_items

    @property
    def items(self) -> List[str]:
        return list(self._items)

    @property
    def count(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Topics) and self._items == other._items

    def __hash__(self) -> int:
        return hash(tuple(self._items))

    def __repr__(self) -> str:
        return f"<Topics {self._items}>"
