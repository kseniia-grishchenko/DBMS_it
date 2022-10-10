import PySimpleGUI as sg

from models import column
from models.db_manager import DBManager
from ui.views import (
    create_db_view,
    add_table_view,
    add_column_view,
    add_row_view,
    enum_column_view,
    delete_row_view,
    delete_table_view,
    change_row_view,
    change_row_detailed_view,
    save_db_view,
    open_db_view,
    find_rows_view,
)

sg.set_options(font=("Andale Mono", 14))

layout = [
    [sg.Button("Create DB"), sg.Button("Open DB"), sg.Button("Save DB")],
    [
        sg.Text("Current DB:"),
        sg.Text(key="-CURRENT-DB-"),
        sg.Text(key="-ERRORS-", text_color="red"),
    ],
    [
        sg.Text("Tables:"),
        sg.Text("Data:", pad=((145, 0), (0, 0))),
        sg.Button("Add Column"),
        sg.Push(),
        sg.Button("Find Rows"),
    ],
    [
        sg.Listbox([], size=(23, 16), key="-TABLE-LIST-", enable_events=True),
        sg.Multiline(key="-TABLE-DATA-", size=(80, 16), font=("Andale Mono", 15)),
    ],
    [
        sg.Button("Add Table"),
        sg.Button("Delete Table"),
        sg.Button("Add Row"),
        sg.Button("Delete Row"),
        sg.Button("Change Row"),
    ],
]


def parse_value(val, type_: str):
    if type_ == "int":
        return int(val)
    if type_ == "real":
        return float(val)

    return val


DB_MANAGER = DBManager()
LOCAL_DATA = {"selected_table": None}

window = sg.Window("DBMS", layout)

while True:
    try:
        event, values = window.read()
        should_re_render = True
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == "Create DB":
            event, values = create_db_view()
            if event == "OK":
                DB_MANAGER.create_database(values["-DB-NAME-"])

        elif event == "Add Table":
            event, values = add_table_view()
            if event == "OK":
                DB_MANAGER.add_table(values["-TABLE-NAME-"])
                LOCAL_DATA["selected_table"] = values["-TABLE-NAME-"]

        elif event == "Delete Table":
            event, values = delete_table_view()
            if event == "OK":
                DB_MANAGER.delete_table(values["-TABLE-NAME-"])
                LOCAL_DATA["selected_table"] = None

        elif event == "Add Column":
            event, values = add_column_view(
                column_choices=column.COLUMN_TYPE_CHOICES,
                table_name=LOCAL_DATA["selected_table"],
            )
            if event == "OK":
                new_column = None
                column_type = values["-COLUMN-TYPE-"]
                one_input_columns = {
                    "int": column.IntCol,
                    "real": column.RealCol,
                    "char": column.CharCol,
                    "string": column.StringCol,
                    "email": column.EmailCol,
                }

                if column_type in one_input_columns:
                    new_column = one_input_columns[column_type](values["-COLUMN-NAME-"])
                elif column_type == "enum":
                    enum_event, enum_values = enum_column_view(
                        values["-COLUMN-NAME-"], list(one_input_columns)
                    )
                    if enum_event == "OK":
                        new_column_type = enum_values["-COLUMN-TYPE-"]
                        # prepare available_values:
                        available_values = enum_values["-AVAILABLE-VALUES-"].split(";")
                        for index, value in enumerate(available_values):
                            available_values[index] = parse_value(
                                value, new_column_type
                            )

                        new_column = column.EnumCol(
                            name=values["-COLUMN-NAME-"],
                            column_type=enum_values["-COLUMN-TYPE-"],
                            available_values=available_values,
                            default=parse_value(
                                enum_values["-DEFAULT-VALUE-"], new_column_type
                            ),
                        )

                DB_MANAGER.add_column(values["-TABLE-NAME-"], new_column)
                LOCAL_DATA["selected_table"] = values["-TABLE-NAME-"]

        elif event == "Add Row":
            table = DB_MANAGER.get_table(LOCAL_DATA["selected_table"])
            event, values = add_row_view(
                table.columns[1:],  # index is not writable
            )
            if event == "OK":
                # prepare data
                for column_name in list(values):
                    correct_column_name = column_name.split(":")[0]
                    col = table.get_column_by_name(correct_column_name)
                    values[correct_column_name] = parse_value(
                        values.pop(column_name), col.type
                    )

                DB_MANAGER.add_row(table_name=table.name, data=values)

        elif event == "Delete Row":
            event, values = delete_row_view()
            if event == "OK":
                DB_MANAGER.delete_row(
                    LOCAL_DATA["selected_table"], int(values["-ROW-INDEX-"])
                )

        elif event == "Change Row":
            table = DB_MANAGER.get_table(LOCAL_DATA["selected_table"])
            event, values = change_row_view()
            if event == "OK":
                index_to_change = int(values["-ROW-INDEX-"])
                change_event, change_values = change_row_detailed_view(
                    table.columns[1:],
                    table.get_row(index_to_change).values,
                )
                if change_event == "OK":
                    # prepare data
                    for column_name in list(change_values):
                        correct_column_name = column_name.split(":")[0]
                        col = table.get_column_by_name(correct_column_name)
                        change_values[correct_column_name] = parse_value(
                            change_values.pop(column_name), col.type
                        )

                    DB_MANAGER.change_row(
                        table_name=table.name, index=index_to_change, data=change_values
                    )

        elif event == "Find Rows":
            event, values = find_rows_view()
            if event == "OK":
                view = DB_MANAGER.find_rows(
                    LOCAL_DATA["selected_table"], values["-SEARCH-STRING-"]
                )
                window["-TABLE-DATA-"].update(str(view))
                should_re_render = False

        elif event == "-TABLE-LIST-":  # select table
            if values["-TABLE-LIST-"]:
                LOCAL_DATA["selected_table"] = values["-TABLE-LIST-"][0]

        elif event == "Save DB":
            event, values = save_db_view()

            if event == "OK":
                DB_MANAGER.save_database(values["-DB-SAVE-PATH-"])
                sg.popup("Successfully saved DB!")

        elif event == "Open DB":
            event, values = open_db_view()

            if event == "OK":
                DB_MANAGER.open_database(values["-DB-OPEN-PATH-"])
                sg.popup("Successfully loaded DB!")
                LOCAL_DATA["selected_table"] = None

        # update view
        if should_re_render:
            window["-CURRENT-DB-"].update(DB_MANAGER.db.name)
            window["-TABLE-LIST-"].update(list(DB_MANAGER.db.tables))

            if LOCAL_DATA["selected_table"]:
                table = DB_MANAGER.get_table(LOCAL_DATA["selected_table"])
                window["-TABLE-DATA-"].update(str(table))
            else:
                window["-TABLE-DATA-"].update("")
            window["-ERRORS-"].update("")

    except (TypeError, KeyError, ValueError, IndexError) as e:
        window["-ERRORS-"].update(f"Errors: {e}")


window.close()
