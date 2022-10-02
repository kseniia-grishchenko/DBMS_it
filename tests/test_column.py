from typing import Type

import pytest

from models.column import Column, IntCol, RealCol, CharCol, StringCol, EmailCol, EnumCol


def test_column_default_validation():
    class TestColumn(Column):
        @staticmethod
        def validate(value):
            return value == "correct"

    col = TestColumn("test_type", "test_name", "correct")
    assert col.default == "correct"

    with pytest.raises(TypeError) as exception_info:
        TestColumn("test_type", "test_name", "incorrect")

    assert exception_info.value.args[0] == (
        "This value 'incorrect' does not pass column validation! Column 'test_name' has "
        "type 'test_type' and entered type is 'str'"
    )


def test_int_col_validation():
    col = IntCol("amount")
    assert col.validate(10)
    assert not col.validate("asdf")


def test_float_col_validation():
    col = RealCol("price")
    assert col.validate(10.0)
    assert not col.validate(10)


def test_char_col_validation():
    col = CharCol("class")
    assert col.validate("A")
    assert not col.validate("BCD")


def test_string_col_validation():
    col = StringCol("name")
    assert col.validate("John Snow")
    assert not col.validate(True)


def test_email_col_validation():
    col = EmailCol("name")
    assert col.validate("admin@admin.com")
    assert not col.validate("my_email")


# fmt: off
@pytest.mark.parametrize(
    "args,error_type,error_message",
    [
        (
            ("test", "error_type", (1, 2, 3)),
            TypeError,
            "This type is not supported!"
        ),
        (
            ("test", "int", tuple()),
            ValueError,
            "Available values cannot be empty!"
        ),
        (
            ("test", "int", (1, "asdf", 3)),
            ValueError,
            "Value 'asdf' does not pass validation for 'int' type"
        ),
        (
            ("test", "int", (1, 3, 5), 7),
            TypeError,  # here not sure, maybe also ValueError btw
            "This value '7' does not pass column validation! "
            "Column 'test' has type 'int' and entered type is 'int'"
        )
    ],
)
# fmt: on
def test_enum_col_initialization_errors(
    args: tuple, error_type: Type[Exception], error_message: str
):
    with pytest.raises(error_type) as exception_info:
        EnumCol(*args)

    assert exception_info.value.args[0] == error_message


def test_enum_col_validation():
    col = EnumCol("test", "real", (1.5, 3.0))
    assert col.validate(3.0)
    assert not col.validate(4.5)


def test_enum_col_default_is_first_if_not_provided():
    col = EnumCol("test", "email", ("admin@admin.com", "test@test.com"))
    assert col.default == "admin@admin.com"


@pytest.mark.parametrize(
    "column_class", [IntCol, RealCol, CharCol, StringCol, EmailCol]
)
def test_default_values_pass_validation(column_class):
    assert column_class.validate(column_class.DEFAULT)
