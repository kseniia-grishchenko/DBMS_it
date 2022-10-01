from typing import Any


class Row:
    def __init__(self, values: list[Any]) -> None:
        self.values = values

    def __getitem__(self, index: int) -> Any:
        return self.values[index]

    def __repr__(self) -> str:
        return f'[{", ".join(map(str, self.values))}]'
