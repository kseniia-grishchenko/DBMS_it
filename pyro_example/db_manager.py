from __future__ import annotations
import os

import pickle

import Pyro5
from Pyro5.api import expose, Daemon

from typing import Any

from models import column
from models.database import Database
from models.row import Row
from models.table import Table

from models.db_manager import DBManager

one_input_columns = {
    "int": column.IntCol,
    "real": column.RealCol,
    "char": column.CharCol,
    "string": column.StringCol,
    "email": column.EmailCol,
}


@expose
class RemoteDBManager(DBManager):
    def __init__(self, db: Database = None) -> None:
        self.db = db

    @property
    def db(self) -> Database:
        if self._db is None:
            raise ValueError("You should open or create DB before accessing it!")

        return self._db

    @db.setter
    def db(self, value: Database) -> None:
        self._db = value

    def create_database(self, name: str) -> None:
        self.db = Database(name)
        print(f"Database created: {name}")
        daemon.register(self.db)

    def add_table(self, name: str) -> Table:
        table = self.db.add_table(name)
        table_uri = daemon.register(table)
        print(f"Table added: {name}")
        return table_uri

    def get_table(self, name: str) -> Table:
        table = self.db.get_table(name)
        print(f"Get table: {name}", table)
        return table

    def delete_table(self, name: str) -> Table:
        table = self.db.delete_table(name)
        print(f"Delete table: {name}")
        return daemon.unregister(table)

    def add_column(self, table_name: str, column_type, column_name) -> None:
        new_column = one_input_columns[column_type](column_name)
        table = self.get_table(table_name)
        added_column = table.add_column(new_column)
        column_uri = daemon.register(added_column)
        print(f"Add column: {new_column.name} to table: {table_name}")
        return column_uri

    def add_row(self, table_name: str, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        row = table.add_row(data)
        row_uri = daemon.register(row)
        print(f"Add row: {data} to table: {table_name}")
        return row_uri

    def change_row(self, table_name: str, index: int, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        table.change_row(index, data)
        print(f"Change row: {index} of table: {table_name}")

    def find_rows(self, table_name: str, search_string: str) -> Table:
        table = self.get_table(table_name)
        print(f"Find rows of table: {table_name }by substring: {search_string} ")
        view = table.find_rows(search_string)
        view_uri = daemon.register(view)
        print(f"Found rows: {view}")
        return view_uri

    def delete_row(self, table_name: str, index: int) -> Row:
        table = self.get_table(table_name)
        row = table.delete_row(index)
        print(f"Delete row: {index} from table: {table_name}")
        return daemon.unregister(row)

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

        print("opened db", db)

        self.db = db
        daemon.register(self.db, force=True)

        print("tables", db.tables)
        for table in db.tables.values():
            daemon.register(table, force=True)
            for col in table.columns_obj:
                daemon.register(col, force=True)
            for row in table.rows_obj:
                daemon.register(row, force=True)

        print(f"Open DB from: {path_to_load}")

    def unregister_db(self) -> None:
        print("unregister")
        daemon.unregister(self.db)


daemon = Daemon()
uri = daemon.register(RemoteDBManager)

print("Ready. Object uri =", uri)
daemon.requestLoop()
# /Users/ksishka/Documents/university/4nd_course/it/dbms/pyro_example/temp
