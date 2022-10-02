import pytest

from models.column import IntCol, EmailCol, EnumCol, StringCol, CharCol
from models.table import Table


def test_add_column():
    table = Table("test")

    assert table.columns_count == 0

    test_col = IntCol("amount")

    table.add_column(test_col)

    assert table.columns_count == 1

    with pytest.raises(ValueError) as exception_info:
        table.add_column(test_col)

    assert (
        exception_info.value.args[0]
        == "Column with name 'amount' already exists in the table!"
    )


def test_add_row():
    table = Table("test")

    assert table.rows_count == 0

    with pytest.raises(ValueError) as exception_info:
        table.add_row({})

    assert exception_info.value.args[0] == "Row data cannot be empty!"

    with pytest.raises(ValueError) as exception_info:
        table.add_row({"amount": 1})

    assert (
        exception_info.value.args[0]
        == "Invalid column names: ('amount',) is not subset of ()!"
    )

    table.add_column(IntCol("amount"))
    table.add_row({"amount": 10})
    assert table.get_row(0).values == [10]

    with pytest.raises(TypeError):
        table.add_row({"amount": "hello"})


def test_add_column_after_add_row():
    table = Table("test")
    table.add_column(IntCol("amount"))
    table.add_row({"amount": 1})

    assert table.rows_count == 1
    assert table.get_row(0).values == [1]

    table.add_column(EmailCol("user_email"))
    table.add_row({"amount": 2, "user_email": "test@test.com"})

    assert table.rows_count == 2
    assert table.get_row(0).values == [1, "default@default.com"]
    assert table.get_row(1).values == [2, "test@test.com"]


def test_table_str():
    table = Table("test")
    assert str(table) == "Table: test\n"

    table.add_column(IntCol("amount"))
    assert (
        str(table)
        == """Table: test
| index   | amount   |
|---------+----------|"""
    )

    table.add_column(EmailCol("email"))
    assert (
        str(table)
        == """Table: test
| index   | amount   | email   |
|---------+----------+---------|"""
    )

    table.add_row({"amount": 10, "email": "admin@admin.com"})
    table.add_row({"amount": 15, "email": "user@user.com"})
    assert (
        str(table)
        == """Table: test
|   index |   amount | email           |
|---------+----------+-----------------|
|       0 |       10 | admin@admin.com |
|       1 |       15 | user@user.com   |"""
    )


def test_change_row():
    table = Table("test")
    table.add_column(IntCol("amount"))
    table.add_column(
        EnumCol("user_type", "string", ("admin", "user", "moderator"), "user")
    )

    table.add_row({"amount": 10, "user_type": "admin"})
    table.add_row({"amount": 20})

    assert table.get_row(1).values == [20, "user"]

    with pytest.raises(ValueError):
        table.change_row(0, {})

    with pytest.raises(IndexError) as exception_info:
        table.change_row(10, {"amount": 10})

    assert exception_info.value.args[0] == "Row with index '10' does not exist!"

    with pytest.raises(ValueError):
        table.change_row(1, {"non_existing_column": "data"})

    with pytest.raises(TypeError):
        table.change_row(1, {"amount": "incorrect_type_value"})

    with pytest.raises(TypeError):
        table.change_row(1, {"user_type": "non_existing_user_type"})

    table.change_row(1, {"amount": 30, "user_type": "moderator"})
    assert table.get_row(1).values == [30, "moderator"]


def test_find_rows():
    table = Table("test")
    table.add_column(IntCol("amount"))
    table.add_column(StringCol("username"))
    table.add_column(CharCol("class"))

    table.add_row({"amount": 10, "username": "user1", "class": "A"})
    table.add_row({"amount": 20, "username": "user2", "class": "B"})
    table.add_row({"amount": 15, "username": "user3", "class": "A"})
    table.add_row({"amount": 25, "username": "admin", "class": "D"})

    view = table.find_rows("user")
    assert view.columns_count == 3
    assert view.rows_count == 3

    view = table.find_rows("A")
    assert view.columns_count == 3
    assert view.rows_count == 2

    view = table.find_rows("5")
    assert view.columns_count == 3
    assert view.rows_count == 0
