import argparse
import html
import re
from functools import partial
from multiprocessing import Pool
from typing import List, Union

from .constants.leetcode_to_neetcode import LEETCODE_TO_NEETCODE
from .queries import get_data, get_slug, get_url


def sanitize(input: Union[str, list, None]) -> Union[str, list]:
    """
    Sanitize the given input to be Anki-compatible. This includes
    removing delimeters with the desired Anki delimeter chosen
    by the user.

    Arguments
    ---------
    input : str
        The input to sanitize.

    Returns
    -------
    str
        The sanitized input.
    """
    if input is None:
        return ""
    if isinstance(input, list):
        return input
    input = html.unescape(input)
    input = re.sub(r"[;\n]", " ", input)
    input = input.replace("</strong>", "</strong><br>")
    input = re.sub(r"(<br>){2,}", "<br>", input)
    return input


def generate_solution_link(slug: str, solution_id: str) -> str:
    """
    Generate a link to the LeetCode solution with the given ID.

    Arguments
    ---------
    slug : str
        The slug of the question to generate a link for.
    solution_id : str
        The ID of the solution to generate a link for.

    Returns
    -------
    str
        The link to the LeetCode solution with the given ID.
    """
    return f"https://leetcode.com/problems/{slug}/solutions/{solution_id}/1/"


def save_output(
    problems: List[Union[str, None]], file: str, format: str = "cards"
) -> None:
    with open(file, "w") as f:
        for problem in problems:
            if problem:
                f.write(problem + "\n")


def generate_problem(
    url: str, language: Union[str, None] = None, format: str = "cards"
) -> Union[str, None]:
    """
    Generates a problem strings for the given URL in the requested format

    Arguments
    ---------
    url : str
        The URL of the question to generate a problem for.
    language : str
        The coding language to generate a problem for.

    Returns
    -------
    str
        The problem for the given URL.
    """
    url = url.strip()
    if not url:
        return None
    slug = get_slug(url)
    if language:
        language = language.strip().lower()
    try:
        data = get_data(slug, language)
    except Exception as e:
        print(f"Failed to generate problem for {url}: {e}")
        return None

    data = {k: sanitize(v) for k, v in data.items()}

    problem = (
        f"<h1><a href=\"{get_url(url)}\">{data['id']}."
        f" {data['title']}</a></h1>{data['content']}<br>"
    )
    if data["companies"]:
        for company in data["companies"]:
            problem += company["name"]
    problem += "<ul>"
    problem += "<strong>Tags:</strong><br>"
    for tag in data["tags"]:
        problem += f"<li>{tag['name']}</li>"
    problem += "</ul>;"
    problem += "<ul>"
    if str(data["id"]) in LEETCODE_TO_NEETCODE:
        neetcode = LEETCODE_TO_NEETCODE[str(data["id"])]
        problem += "<strong>NeetCode Solution:</strong><br>"
        problem += f"<a href=\"{neetcode['url']}\">{neetcode['title']}</a></li><br><br>"

    problem += "<strong>LeetCode User Solutions:</strong><br>"

    for solution in data["solutions"]:
        solution_url = generate_solution_link(slug, solution["id"])
        problem += f'<li><a href="{solution_url}">{solution_url}</a></li>'
    problem += "</ul>;"
    problem += " ".join([tag["slug"] for tag in data["tags"]])

    return problem


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments.

    Returns
    -------
    argparse.Namespace
        The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generates problems from LeetCode questions in a desired format."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    input = parser.add_mutually_exclusive_group(required=True)

    input.add_argument(
        "--url",
        "-u",
        type=str,
        help=(
            "The URL(s) or slug(s) of the LeetCode question(s) to generate"
            " problem(s) for."
        ),
    )

    input.add_argument(
        "--file",
        "-f",
        type=str,
        help=(
            "The file containing the URL(s) or slug(s) of the LeetCode"
            " question(s) to generate problem(s) for."
        ),
    )

    parser.add_argument(
        "--format",
        "-F",
        type=str,
        default="cards",
        choices=["cards"],
        help="The format to save the Anki problem(s) in.",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output.txt",
        help="The output file to write the problem(s) to.",
    )

    parser.add_argument(
        "--language",
        "-l",
        type=str,
        help="The language to generate problem(s) for.",
    )

    return parser.parse_args()


def cli(args: argparse.Namespace):
    """
    Handles the multi-processing of problem generation.
    """
    if args.url:
        urls = args.url.split(",")
    elif args.file:
        with open(args.file, "r") as f:
            urls = f.read().splitlines()

    with Pool() as pool:
        problems = pool.map(
            partial(generate_problem, language=args.language),
            urls,
        )

    save_output(problems, args.output, args.format)


def main():
    args = parse_args()
    cli(args)


if __name__ == "__main__":
    main()
