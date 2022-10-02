from typing import Any


class Row:
    def __init__(self, values: list[Any]) -> None:
        self.values = values

    def __getitem__(self, index: int) -> Any:
        return self.values[index]

    def __setitem__(self, key: int, value: Any) -> None:
        self.values[key] = value

    def __repr__(self) -> str:
        return f'[{", ".join(map(str, self.values))}]'
