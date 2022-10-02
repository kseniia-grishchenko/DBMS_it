from __future__ import annotations

from typing import Any

from tabulate import tabulate

from .column import Column
from .row import Row


class Table:
    def __init__(self, name: str) -> None:
        self._name = name
        self._columns: list[Column] = []
        self._rows: list[Row] = []

    @property
    def name(self):
        return self._name

    @property
    def rows_count(self):
        return len(self._rows)

    @property
    def columns_count(self):
        return len(self._columns)

    def __str__(self):
        return f"Table: {self.name}\n" + self._str_columns_and_rows()

    def _str_columns_and_rows(self) -> str:
        if len(self._columns) == 0:
            return ""

        return tabulate(
            [[index] + row.values for index, row in enumerate(self._rows)],
            ("index",) + self._get_column_names(),
            tablefmt="orgtbl",
        )

    def _get_column_names(self) -> tuple[str]:
        return tuple(column.name for column in self._columns)

    def _check_column_name_already_exists(self, new_column_name: str) -> bool:
        return new_column_name in self._get_column_names()

    def add_column(self, column: Column) -> None:
        if self._check_column_name_already_exists(column.name):
            raise ValueError(
                f"Column with name '{column.name}' already exists in the table!"
            )

        self._columns.append(column)
        self._add_default_values_to_all_existing_rows(column)

    def _add_default_values_to_all_existing_rows(self, column: Column) -> None:
        for row in self._rows:
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

        for column in self._columns:
            value_to_add = data.get(column.name, None)

            if not value_to_add:  # handle default case
                row.append(column.default)
                continue

            column.validate_or_error(value_to_add)

            row.append(value_to_add)

        self._rows.append(Row(row))

    def get_row(self, index: int) -> Row:
        if not (0 <= index < len(self._rows)):
            raise IndexError(f"Row with index '{index}' does not exist!")

        return self._rows[index]

    def _get_column_by_name(self, name: str) -> Column:
        return next(column for column in self._columns if column.name == name)

    def change_row(self, index: int, data: dict) -> None:
        row = self.get_row(index)
        self._validate_row_data(data)

        # validate all values pass validation
        for column_name, new_column_value in data.items():
            column = self._get_column_by_name(column_name)
            column.validate_or_error(new_column_value)

        for column_name, new_column_value in data.items():
            column_index = self._get_column_names().index(column_name)
            row[column_index] = new_column_value

    def find_rows(self, search_string: str) -> Table:
        """Find rows (and create a temp Table) using search_string - case sensitive contains check for string columns"""
        view = Table("view")
        view._columns = self._columns

        view._rows = [
            row
            for row in self._rows
            if any(
                search_string in value for value in row.values if isinstance(value, str)
            )
        ]

        return view
