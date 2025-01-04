import os
from datetime import date
from typing import List, Union

import xlsxwriter


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
    problems : List[Union[List[str], None]]
        The problems to save.
    file : str
        The file to save the problems to.
    """
    if os.path.exists(file + ".xlsx"):
        os.remove(file + ".xlsx")
    workbook = xlsxwriter.Workbook(file + ".xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "Title")
    worksheet.write(0, 2, "Difficulty")
    worksheet.write(
        0,
        3,
        "Url",
    )
    worksheet.write(0, 4, "Date Attempted")
    worksheet.write(0, 5, "Tags")
    worksheet.write(0, 6, "Neetcode")
    worksheet.write(0, 7, "Solutions")
    worksheet.write(0, 8, "Companies")

    # Add bold formatting to the first row
    bold = workbook.add_format({"bold": True})
    worksheet.set_row(0, None, bold)

    # Add formatting based on the difficulty
    worksheet.conditional_format(
        1,
        2,
        len(problems),
        2,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": "Easy",
            "format": workbook.add_format({"bg_color": "#00FF00"}),
        },
    )
    worksheet.conditional_format(
        1,
        2,
        len(problems),
        2,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": "Medium",
            "format": workbook.add_format({"bg_color": "#FFFF00"}),
        },
    )
    worksheet.conditional_format(
        1,
        2,
        len(problems),
        2,
        {
            "type": "cell",
            "criteria": "equal to",
            "value": "Hard",
            "format": workbook.add_format({"bg_color": "#FF0000"}),
        },
    )

    # Add gradient formatting to the date attempted row
    worksheet.conditional_format(
        1,
        4,
        len(problems),
        4,
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
            for j, line in enumerate(problem):
                if type(line) is date and j == 3:
                    worksheet.write_datetime(i, j, line, date_format)
                else:
                    worksheet.write(i, j, line)

    workbook.close()


SAVE_MAP = {
    "anki": save_string,
    "quizlet": save_string,
    "excel": save_excel,
}
