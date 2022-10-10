from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
from typing import Any


COLUMN_TYPE_CHOICES = ["int", "real", "char", "string", "email", "enum"]


@dataclass
class Column(ABC):
    type: str
    name: str
    default: Any

    def __post_init__(self) -> None:
        self.validate_or_error(self.default)

    @staticmethod
    @abstractmethod
    def validate(value) -> bool:
        pass

    def validate_or_error(self, value: Any) -> None:
        if not self.validate(value):
            raise TypeError(
                f"This value '{value}' does not pass column validation! "
                f"Column '{self.name}' has type '{self.type}' and entered type is "
                f"'{type(value).__name__}'"
            )


class IntCol(Column):
    TYPE = "int"
    DEFAULT = 0

    def __init__(self, name: str, default: int = DEFAULT) -> None:
        super().__init__(IntCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, int)


class RealCol(Column):
    TYPE = "real"
    DEFAULT = 0.0

    def __init__(self, name: str, default: float = DEFAULT) -> None:
        super().__init__(RealCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, float)


class CharCol(Column):
    TYPE = "char"
    DEFAULT = "_"

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(CharCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str) and len(value) == 1


class StringCol(Column):
    TYPE = "string"
    DEFAULT = ""

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(StringCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str)


class EmailCol(Column):
    TYPE = "email"
    DEFAULT = "default@default.com"

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(EmailCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
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
    ) -> None:
        if len(available_values) == 0:
            raise ValueError("Available values for enum cannot be empty!")

        if default is None:
            default = available_values[0]

        if column_type not in EnumCol.COLUMN_TYPE_CLASS.keys():
            raise TypeError(
                f"Type '{column_type}' is not supported for enum! Please use one of {tuple(EnumCol.COLUMN_TYPE_CLASS)}"
            )

        type_class: Column = EnumCol.COLUMN_TYPE_CLASS[column_type]

        for value in available_values:
            if not type_class.validate(value):
                raise ValueError(
                    f"Value '{value}' does not pass validation for '{column_type}' type"
                )

        self.available_values = available_values
        self.type_class = type_class
        super().__init__(column_type, name, default)

    def validate(self, value) -> bool:
        return value in self.available_values and self.type_class.validate(value)
