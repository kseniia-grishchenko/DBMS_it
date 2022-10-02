from __future__ import annotations

from typing import Any

from models.column import Column
from models.database import Database
from models.row import Row
from models.table import Table


class DBManager:
    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def create_database(name: str) -> DBManager:
        return DBManager(Database(name))

    def add_table(self, name: str) -> None:
        return self.db.add_table(name)

    def get_table(self, name: str) -> Table:
        return self.db.get_table(name)

    def delete_table(self, name: str) -> Table:
        return self.db.delete_table(name)

    def add_column(self, table_name: str, column: Column) -> None:
        table = self.get_table(table_name)
        return table.add_column(column)

    def add_row(self, table_name: str, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        return table.add_row(data)

    def change_row(self, table_name: str, index: int, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        return table.change_row(index, data)

    def find_rows(self, table_name: str, search_string: str) -> Table:
        table = self.get_table(table_name)
        return table.find_rows(search_string)

    def delete_row(self, table_name: str, index: int) -> Row:
        table = self.get_table(table_name)
        return table.delete_row(index)
