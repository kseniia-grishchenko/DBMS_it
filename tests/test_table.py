import pytest

from models.column import IntCol, EmailCol
from models.table import Table


def test_add_column():
    table = Table("test")

    assert len(table.columns) == 0

    test_col = IntCol("amount")

    table.add_column(test_col)

    assert len(table.columns) == 1

    with pytest.raises(ValueError) as exception_info:
        table.add_column(test_col)

    assert (
        exception_info.value.args[0]
        == "Column with name 'amount' already exists in the table!"
    )


def test_add_row():
    table = Table("test")

    assert len(table.rows) == 0

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
    assert table.rows[0].values == [10]

    with pytest.raises(TypeError):
        table.add_row({"amount": "hello"})


def test_add_column_after_add_row():
    table = Table("test")
    table.add_column(IntCol("amount"))
    table.add_row({"amount": 1})

    assert len(table.rows) == 1
    assert table.rows[0].values == [1]

    table.add_column(EmailCol("user_email"))
    table.add_row({"amount": 2, "user_email": "test@test.com"})

    assert len(table.rows) == 2
    assert table.rows[0].values == [1, "default@default.com"]
    assert table.rows[1].values == [2, "test@test.com"]


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
