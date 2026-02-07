from datetime import date
from pathlib import Path
from typing import List, Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from leetcode_study_tool.leetcode_to_neetcode import LEETCODE_TO_NEETCODE
from leetcode_study_tool.queries import get_url

template_dir = Path(__file__).parent / "templates"
env = Environment(
    loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "xml"])
)


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


def render_template(
    template_path: Optional[str], template_name: Optional[str], **kwargs
) -> str:
    """
    Render a template with the given context

    Arguments
    ---------
    template_path : Optional[str]
        Path to a custom template file. If None, use built-in templates.
    template_name : str
        Name of the built-in template to use if template_path is None.
    kwargs : dict
        Template context variables.

    Returns
    -------
    str
        Rendered template content.
    """
    if not template_path and not template_name:
        raise ValueError("Either template_path or template_name must be provided")
    if template_path:
        custom_dir = Path(template_path).parent
        custom_file = Path(template_path).name
        custom_env = Environment(
            loader=FileSystemLoader(custom_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = custom_env.get_template(custom_file)
    else:
        assert template_name is not None
        template = env.get_template(template_name)

    kwargs["solution_url"] = format_solution_link
    return template.render(**kwargs)


def format_anki(
    url: str, slug: str, data: dict, template_path: Optional[str] = None
) -> str:
    """
    formats an Anki problem using Jinja template

    Arguments
    ---------
    url : str
        The URL of the question to format a problem for.
    slug : str
        The slug of the question to format a problem for.
    data : dict
        The data of the question to format a problem for.
    template_path : Optional[str]
        Path to a custom template file. If None, use built-in templates.

    Returns
    -------
    str
        The formatted Anki problem.
    """
    neetcode = LEETCODE_TO_NEETCODE.get(str(data["id"]))

    rendered = render_template(
        template_path,
        "anki.html.j2",
        url=get_url(url),
        slug=slug,
        data=data,
        neetcode=neetcode,
    )
    rendered = rendered.replace("\n", "<br>")
    rendered = rendered.replace("\t", "\u00a0\u00a0\u00a0\u00a0")
    rendered = " ".join(rendered.split())
    return rendered


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
        [id, title, difficulty, url, date attempted, tags, video_url, short_url, solutions, companies]
    """
    row = []
    row.append(data["id"])
    row.append(data["title"])
    row.append(data["difficulty"])
    row.append(get_url(url))
    row.append(date.today())
    row.append(", ".join([tag["name"] for tag in data["tags"]]))
    if str(data["id"]) in LEETCODE_TO_NEETCODE:
        neetcode_data = LEETCODE_TO_NEETCODE[str(data["id"])]
        # Add regular video URL
        video_url = neetcode_data.get("video", {}).get("url", "")
        row.append(video_url)
        # Add shorts URL in new column
        short_url = neetcode_data.get("short", {}).get("url", "")
        row.append(short_url)
    else:
        row.append("")  # No regular video
        row.append("")  # No short
    row.append(data.get("neetcode_solution", ""))
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

__all__ = [
    "format_solution_link",
    "format_anki",
    "format_quizlet",
    "format_excel",
    "FORMAT_MAP",
    "render_template",
]
