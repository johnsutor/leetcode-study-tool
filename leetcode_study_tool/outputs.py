from typing import List, Union


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
    print("foo")
    with open(file + ".txt", "w") as f:
        for problem in problems:
            if problem:
                f.write(problem + "\n")


def save_excel(problems: List[Union[str, None]], file: str) -> None:
    """
    Save the given problems to the given Excel file.

    Arguments
    ---------
    problems : List[Union[str, None]]
        The problems to save.
    file : str
        The file to save the problems to.
    """
    pass


SAVE_MAP = {
    "anki": save_string,
    "quizlet": save_string,
    "excel": save_excel,
}
