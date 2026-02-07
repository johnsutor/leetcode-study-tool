import os
from datetime import date
from typing import List, Union

import xlsxwriter

from leetcode_study_tool.formatters import (
    DATE_COLUMN_INDEX,
    DIFFICULTY_COLUMN_INDEX,
    EXCEL_COLUMNS,
)


def save_string(problems: List[Union[str, None]], file: str) -> None:
    """
    Save the given problems to the given file.

    Arguments
    ---------
    problems : List[Union[str, None]]
        The problems to save.
    file : str
        The file to save the problems to.
    """
    with open(file + ".txt", "w") as f:
        for problem in problems:
            if problem:
                f.write(problem + "\n")


def save_excel(problems: List[Union[List[Union[str, date]], None]], file: str) -> None:
    """
    Save the given problems to the given Excel file.

    Arguments
    ---------
    problems : List[Union[List[Union[str, date]], None]]
        The problems to save.
    file : str
        The file to save the problems to.
    """
    if os.path.exists(file + ".xlsx"):
        os.remove(file + ".xlsx")
    workbook = xlsxwriter.Workbook(file + ".xlsx")
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({"bold": True})
    for col, header in enumerate(EXCEL_COLUMNS):
        worksheet.write(0, col, header, bold)

    last_row = len(problems)
    diff_col = DIFFICULTY_COLUMN_INDEX
    date_col = DATE_COLUMN_INDEX

    worksheet.conditional_format(
        1,
        diff_col,
        last_row,
        diff_col,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": '"Easy"',
            "format": workbook.add_format({"bg_color": "#00FF00"}),
        },
    )
    worksheet.conditional_format(
        1,
        diff_col,
        last_row,
        diff_col,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": '"Medium"',
            "format": workbook.add_format({"bg_color": "#FFFF00"}),
        },
    )
    worksheet.conditional_format(
        1,
        diff_col,
        last_row,
        diff_col,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": '"Hard"',
            "format": workbook.add_format({"bg_color": "#FF0000"}),
        },
    )

    worksheet.conditional_format(
        1,
        date_col,
        last_row,
        date_col,
        {
            "type": "3_color_scale",
            "min_color": "red",
            "mid_color": "yellow",
            "max_color": "green",
        },
    )

    date_format = workbook.add_format({"num_format": "dd/mm/yy"})

    for i, problem in enumerate(problems, start=1):
        if problem:
            for j, cell in enumerate(problem):
                if isinstance(cell, date):
                    worksheet.write_datetime(i, j, cell, date_format)
                else:
                    worksheet.write(i, j, cell)

    workbook.close()


SAVE_MAP = {
    "anki": save_string,
    "excel": save_excel,
}
