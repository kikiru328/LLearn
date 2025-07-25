from typing import List, Any


class Topics:
    __slots__ = ("_items",)

    def __init__(self, raw: List[Any]) -> None:
        if (
            not isinstance(raw, list)
            or len(raw) == 0
            or any(not isinstance(item, str) or not item.strip() for item in raw)
        ):
            raise ValueError("Topics must be a non-empty list of non-blank strings")
        # 스트립해서 저장
        self._items = [item.strip() for item in raw]

    @property
    def items(self) -> List[str]:
        return list(self._items)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Topics) and self._items == other._items

    def __hash__(self) -> int:
        return hash(tuple(self._items))

    def __repr__(self) -> str:
        return f"<Topics {self._items}>"
