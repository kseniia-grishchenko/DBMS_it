from models.column import IntCol, RealCol, CharCol, StringCol, EnumCol, EmailCol
from models.row import Row
from models.table import Table


if __name__ == "__main__":
    int_col = IntCol("amount")
    int_res = int_col.validate("agnbfbnfg")

    real_col = RealCol("weight")
    real_res = real_col.validate(111.3)

    char_col = CharCol("letter")
    char_res = char_col.validate("aa")

    string_col = StringCol("word")
    string_res = string_col.validate("iweoweie9409u3r4uaa")

    enum_col = EnumCol("enum", [1, 100, 1000])
    enum_res = enum_col.validate(2)

    email_col = EmailCol("email")
    email_res = email_col.validate("test@gmail.com")

    row = Row(["a", 1, "bcaa", "test"])

    # print(row[3])
    #
    # print(int_res)
    # print(real_res)
    # print(char_res)
    # print(string_res)
    # print(enum_res)
    # print(email_res)

    test_table = Table("test")
    #
    # print(test_table.columns)

    test_table.add_column("int", "amount")
    test_table.add_column("char", "short_symbol")
    test_table.add_column("real", "weight")
    test_table.add_column("enum", "available_colors", ["red", "pink", "blue"])
    # print(test_table.columns)

    try:
        test_table.add_row({"amount": 4})
        test_table.add_row({"short_symbol": "a", "available_colors": "pink"})
    except Exception as e:
        print(e)

    print(test_table)
    test_table.change_row(0, {"short_symbol": "b"})
