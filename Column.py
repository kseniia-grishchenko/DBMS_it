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
    default = 0
    type = 'int'

    def __init__(self, name):
        super().__init__(IntCol.type, name, IntCol.default)

    def validate(self, value):
        return isinstance(value, int)


class RealCol(Column):
    default = 0.0
    type = 'real'

    def __init__(self, name):
        super().__init__(RealCol.type, name, RealCol.default)

    def validate(self, value):
        return isinstance(value, float)


class CharCol(Column):
    default = ''
    type = 'char'

    def __init__(self, name):
        super().__init__(CharCol.type, name, CharCol.default)

    def validate(self, value):
        return isinstance(value, str) and len(value) == 1


class StringCol(Column):
    default = ''
    type = 'string'

    def __init__(self, name):
        super().__init__(StringCol.type, name, StringCol.default)

    def validate(self, value):
        return isinstance(value, str)


class EnumCol(Column):
    type = 'enum'

    def __init__(self, name, values):
        super().__init__(EnumCol.type, name, values[0])
        self.availableValues = values

    def validate(self, value):
        return value in self.availableValues


class EmailCol(Column):
    default = ''
    type = 'email'

    def __init__(self, name):
        super().__init__(EmailCol.type, name, EmailCol.default)

    def validate(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return bool(re.fullmatch(regex, value))

