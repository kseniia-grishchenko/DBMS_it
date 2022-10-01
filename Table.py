from tabulate import tabulate

from Column import IntCol, RealCol, CharCol, StringCol, EnumCol, EmailCol
from Row import Row

COLUMN_TYPES = ["int", "real", "char", "string", "enum", "email"]


class Table:
    columns = []
    rows = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        str_columns = " ".join(map(str, self.columns))
        str_rows = "\n".join(map(str, self.rows))

        return f'[{str_columns}]\n{str_rows}'

    def add_row(self, values):
        row = []
        if len(self.columns) == 0:
            raise ValueError("No column in table")
        if len(values.keys()) > len(self.columns):
            raise ValueError("Values length is bigger then column length")
        for index, column in enumerate(self.columns):
            current_value = values.get(column.name, None)
            if not current_value:
                default_value = column.default
            if current_value and not column.validate(current_value):
                raise TypeError(
                    f"This value {current_value} does not match column type! "
                    f"Column {column.name} type is {column.type} and entered type is {type(current_value)}"
                )
            row.append(current_value or default_value)
        new_row = Row(row)
        self.rows.append(new_row)

    def add_column(self, column_type, name, values=None):
        if values is None:
            values = []
        if column_type not in COLUMN_TYPES:
            raise TypeError(
                "This type is not allowed! Please use one of the next ones: 'int', 'real', 'char', "
                "'string', 'enum', 'email'"
            )
        column = self.create_column(name, column_type, values)
        self.columns.append(column)

    def create_column(self, name, column_type, values=None):
        if values is None:
            values = []
        if column_type == "int":
            return IntCol(name)
        elif column_type == "real":
            return RealCol(name)
        elif column_type == "char":
            return CharCol(name)
        elif column_type == "string":
            return StringCol(name)
        elif column_type == "enum":
            return EnumCol(name, values)
        elif column_type == "email":
            return EmailCol(name)
        else:
            raise TypeError('This type is not supported!')
