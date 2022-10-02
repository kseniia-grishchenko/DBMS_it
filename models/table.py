from typing import Any

from tabulate import tabulate

from .column import Column
from .row import Row


class Table:
    def __init__(self, name: str) -> None:
        self.name = name
        self.columns: list[Column] = []
        self.rows: list[Row] = []

    def __str__(self):
        return f"Table: {self.name}\n" + self._str_columns_and_rows()

    def _str_columns_and_rows(self) -> str:
        if len(self.columns) == 0:
            return ""

        return tabulate(
            [[index] + row.values for index, row in enumerate(self.rows)],
            ("index",) + self._get_column_names(),
            tablefmt="orgtbl",
        )

    def _get_column_names(self) -> tuple[str]:
        return tuple(column.name for column in self.columns)

    def _check_column_name_already_exists(self, new_column_name: str) -> bool:
        return new_column_name in self._get_column_names()

    def add_column(self, column: Column) -> None:
        if self._check_column_name_already_exists(column.name):
            raise ValueError(
                f"Column with name '{column.name}' already exists in the table!"
            )

        self.columns.append(column)
        self._add_default_values_to_all_existing_rows(column)

    def _add_default_values_to_all_existing_rows(self, column: Column) -> None:
        for row in self.rows:
            row.values.append(column.default)

    def _validate_row_data(self, data: dict[str, Any]) -> None:
        if len(data) == 0:
            raise ValueError("Row data cannot be empty!")

        columns_names = self._get_column_names()
        if not set(data.keys()).issubset(set(columns_names)):
            raise ValueError(
                f"Invalid column names: {tuple(data.keys())} is not subset of {columns_names}!"
            )

    def add_row(self, data: dict[str, Any]) -> None:
        self._validate_row_data(data)

        row = []

        for column in self.columns:
            value_to_add = data.get(column.name, None)

            if not value_to_add:  # handle default case
                row.append(column.default)
                continue

            column.validate_or_error(value_to_add)

            row.append(value_to_add)

        self.rows.append(Row(row))

    def get_row(self, index: int) -> Row:
        if not (0 <= index < len(self.rows)):
            raise ValueError("Row with such index does not exist!")

        return self.rows[index]

    def change_row(self, index: int, changed_part: dict) -> None:
        # row exist
        # changed_part len is not 0
        # all keys of changed part is subset of existing columns
        # check all types match
        print(index, changed_part)
        existing_row = self.get_row(index)
        print("Row exists", existing_row)
