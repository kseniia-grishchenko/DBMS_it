from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class Column(ABC):
    type: str
    name: str
    default: Any

    def __post_init__(self):
        if not self.validate(self.default):
            raise TypeError("Default value does not pass validation")

    @staticmethod
    @abstractmethod
    def validate(value):
        pass


class IntCol(Column):
    TYPE = "int"
    DEFAULT = 0

    def __init__(self, name: str, default: int = DEFAULT):
        super().__init__(IntCol.TYPE, name, default)

    @staticmethod
    def validate(value):
        return isinstance(value, int)


class RealCol(Column):
    TYPE = "real"
    DEFAULT = 0.0

    def __init__(self, name: str, default: float = DEFAULT):
        super().__init__(RealCol.TYPE, name, default)

    @staticmethod
    def validate(value):
        return isinstance(value, float)


class CharCol(Column):
    TYPE = "char"
    DEFAULT = "_"

    def __init__(self, name: str, default: str = DEFAULT):
        super().__init__(CharCol.TYPE, name, default)

    @staticmethod
    def validate(value):
        return isinstance(value, str) and len(value) == 1


class StringCol(Column):
    TYPE = "string"
    DEFAULT = ""

    def __init__(self, name: str, default: str = DEFAULT):
        super().__init__(StringCol.TYPE, name, default)

    @staticmethod
    def validate(value):
        return isinstance(value, str)


class EmailCol(Column):
    TYPE = "email"
    DEFAULT = "default@default.com"

    def __init__(self, name: str, default: str = DEFAULT):
        super().__init__(EmailCol.TYPE, name, default)

    @staticmethod
    def validate(value):
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return bool(re.fullmatch(email_regex, value))


class EnumCol(Column):
    TYPE = "enum"

    COLUMN_TYPE_CLASS = {  # this should be frozen dict
        "int": IntCol,
        "real": RealCol,
        "char": CharCol,
        "string": StringCol,
        "email": EmailCol,
    }

    def __init__(
        self, name: str, column_type: str, available_values: tuple, default: Any = None
    ):
        if len(available_values) == 0:
            raise ValueError("Available values cannot be empty!")

        if default is None:
            default = available_values[0]

        if column_type not in EnumCol.COLUMN_TYPE_CLASS.keys():
            raise TypeError("This type is not supported!")

        type_class: Column = EnumCol.COLUMN_TYPE_CLASS[column_type]

        for value in available_values:
            type_class.validate(value)

        super().__init__(column_type, name, default)
        self.available_values = available_values
        self.type_class = type_class

    def validate(self, value):
        return value in self.available_values and self.type_class.validate(value)
