from abc import ABC, abstractmethod
import re


class Column(ABC):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def validate(self, value):
        pass


class IntCol(Column):
    type = 'int'

    def validate(self, value):
        return isinstance(value, int)


class RealCol(Column):
    type = 'real'

    def validate(self, value):
        return isinstance(value, float)


class CharCol(Column):
    type = 'char'

    def validate(self, value):
        return isinstance(value, str) and len(value) == 1


class StringCol(Column):
    type = 'string'

    def validate(self, value):
        return isinstance(value, str)


class EnumCol(Column):
    type = 'enum'

    def __init__(self, name, values):
        super().__init__(name)
        self.availableValues = values

    def validate(self, value):
        return value in self.availableValues


class EmailCol(Column):
    type = 'email'

    def validate(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return bool(re.fullmatch(regex, value))

