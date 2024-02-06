from datetime import date
from textwrap import dedent
from typing import List, Union

from leetcode_study_tool.leetcode_to_neetcode import LEETCODE_TO_NEETCODE  # fmt: skip
from leetcode_study_tool.queries import get_url


def format_list_element(title: str, elements: List[str], is_link: bool = False) -> str:
    """
    formats an HTML list element for the given title and elements

    Arguments
    ---------
    title : str
        The title of the list element to format.
    elements : List[str]
        The elements of the list element to format.

    Returns
    -------
    str
        The formatted list element for the given title and data.
    """
    if is_link:
        return f"""
        <strong>{title}:</strong><br>
        <ul>
            {"".join([ f"<li><a href={item}>" +  item + "</a></li>" for item in elements])}
        </ul>
        """
    return f"""
    <strong>{title}:</strong><br>
    <ul>
        {"".join([ "<li>" +  item + "</li>" for item in elements])}
    </ul>
    """


def format_solution_link(slug: str, solution_id: str) -> str:
    """
    format a link to the LeetCode solution with the given ID.

    Arguments
    ---------
    slug : str
        The slug of the question to format a link for.
    solution_id : str
        The ID of the solution to format a link for.

    Returns
    -------
    str
        The link to the LeetCode solution with the given ID.
    """
    return f"https://leetcode.com/problems/{slug}/solutions/{solution_id}/1/"


def format_anki(url: str, slug: str, data: dict):
    """
    formats an Anki problem for the given URL and data

    Arguments
    ---------
    url : str
        The URL of the question to format a problem for.
    slug : str
        The slug of the question to format a problem for.
    data : dict
        The data of the question to format a problem for.

    Returns
    -------
    str
        The Anki problem for the given URL and data.
    """
    problem = f"""
    <h1>
        <a href=\"{get_url(url)}\">{data['id']}. {data['title']}</a>
    </h1>
    <p>
        {data['content']}
    <p>
    """
    if data["companies"]:
        problem += format_list_element(
            "Companies", [company["name"] for company in data["companies"]]
        )

    if data["tags"]:
        problem += format_list_element("Tags", [tag["name"] for tag in data["tags"]])

    problem += ";"

    if str(data["id"]) in LEETCODE_TO_NEETCODE:
        neetcode = LEETCODE_TO_NEETCODE[str(data["id"])]
        problem += "<strong>NeetCode Solution:</strong><br>"
        problem += f"<a href=\"{neetcode['url']}\">{neetcode['title']}</a></li><br><br>"

    if data["solutions"]:
        problem += format_list_element(
            "LeetCode User Solutions",
            [
                format_solution_link(slug, solution["id"])
                for solution in data["solutions"]
            ],
            is_link=True,
        )

    problem += ";"

    problem += " ".join([tag["slug"].lower() for tag in data["tags"]])

    # Makes code easier to read to remove at the end
    problem = dedent(problem).replace("\n", "")
    return problem


def format_quizlet(url: str, slug: str, data: dict):
    """
    formats a Quizlet problem for the given URL and data

    Arguments
    ---------
    url : str
        The URL of the question to format a problem for.
    slug : str
        The slug of the question to format a problem for.
    data : dict
        The data of the question to format a problem for.

    Returns
    -------
    str
        The Quizlet problem for the given URL and data.
    """
    pass


def format_excel(url: str, slug: str, data: dict) -> List[Union[str, date]]:
    """
    formats an Excel problem for the given URL and data

    Arguments
    ---------
    url : str
        The URL of the question to format a problem for.
    slug : str
        The slug of the question to format a problem for.
    data : dict
        The data of the question to format a problem for.

    Returns
    -------
    str
        The Excel problem for the given URL and data. The problem
        is formatted as a list of strings, where each string is a
        column in the Excel file. This row will have the ordering:
        [id, title, url, date attempted, tags, neetcode, solutions, companies]
    """
    row = []
    row.append(data["id"])
    row.append(data["title"])
    row.append(get_url(url))
    row.append(date.today())
    row.append(", ".join([tag["name"] for tag in data["tags"]]))
    if str(data["id"]) in LEETCODE_TO_NEETCODE:
        neetcode = LEETCODE_TO_NEETCODE[str(data["id"])]
        row.append(neetcode["url"])
    else:
        row.append("")
    row.append(
        "\n".join(
            [
                format_solution_link(slug, solution["id"])
                for solution in data["solutions"]
            ]
        )
    )
    if data.get("companies"):
        row.append(", ".join([company["name"] for company in data["companies"]]))
    else:
        row.append("")
    return row


FORMAT_MAP = {
    "anki": format_anki,
    "quizlet": format_quizlet,
    "excel": format_excel,
}
