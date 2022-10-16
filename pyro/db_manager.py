from __future__ import annotations
import os

import pickle
from Pyro5.api import expose, Daemon

from typing import Any

from models.column import Column
from models.database import Database
from models.row import Row
from models.table import Table

from models.db_manager import DBManager

os.environ["PYRO_SERIALIZER"] = "pickle"


@expose
class RemoteDBManager(DBManager):
    def __init__(self, db: Database = None) -> None:
        self.db = db

    def create_database(self, name: str) -> None:
        self.db = Database(name)
        print(f"Database created: {name}")
        return daemon.register(self.db)

    def add_table(self, name: str) -> None:
        self.db.add_table(name)
        print(f"Table added: {name}")

    def get_table(self, name: str) -> Table:
        table = self.db.get_table(name)
        print(f"Get table: {name}", table)
        return daemon.register(table)

    def delete_table(self, name: str) -> Table:
        table = self.db.delete_table(name)
        print(f"Delete table: {name}")
        return table

    def add_column(self, table_name: str, column: Column) -> None:
        table = self.get_table(table_name)
        table.add_column(column)
        print(f"Add column: {column.name} to table: {table_name}")

    def add_row(self, table_name: str, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        table.add_row(data)
        print(f"Add row: {data} to table: {table_name}")

    def change_row(self, table_name: str, index: int, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        table.change_row(index, data)
        print(f"Change row: {index} of table: {table_name}")

    def find_rows(self, table_name: str, search_string: str) -> Table:
        table = self.get_table(table_name)
        print(f"Find rows of table: {table_name }by substring: {search_string} ")
        rows = table.find_rows(search_string)
        print(f"Found rows: {rows}")
        return rows

    def delete_row(self, table_name: str, index: int) -> Row:
        table = self.get_table(table_name)
        row = table.delete_row(index)
        print(f"Delete row: {index} from table: {table_name}")
        return row

    def save_database(self, path_to_save: str = None) -> str:
        if path_to_save is None:
            path_to_save = f"{self.db.name}.pickle"

        with open(path_to_save, "wb") as file:
            pickle.dump(self.db, file)

        print(f"Save DB to: {path_to_save}")

        return path_to_save

    def open_database(self, path_to_load: str = None) -> None:
        with open(path_to_load, "rb") as file:
            db = pickle.load(file)

        self.db = db

        print(f"Open DB from: {path_to_load}")


daemon = Daemon()
uri = daemon.register(RemoteDBManager)

print("Ready. Object uri =", uri)
daemon.requestLoop()
