from models.table import Table


class Database:
    def __init__(self, name: str):
        self._name = name
        self._tables: dict[str, Table] = {}

    @property
    def name(self):
        return self._name

    @property
    def tables_count(self):
        return len(self._tables)

    def add_table(self, table_name: str) -> None:
        table = Table(table_name)
        if table.name in self._tables:
            raise ValueError(f"Table with name '{table.name}' already exists in DB!")

        self._tables[table.name] = table

    def _validate_table_existence(self, table_name: str) -> None:
        if table_name not in self._tables:
            raise KeyError(f"No table with name '{table_name}' found in DB!")

    def get_table(self, table_name: str) -> Table:
        self._validate_table_existence(table_name)
        return self._tables[table_name]

    def delete_table(self, table_name: str) -> Table:
        table = self.get_table(table_name)
        del self._tables[table_name]
        return table
