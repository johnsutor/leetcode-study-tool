import argparse

from leetcode_study_tool.creator import ProblemsCreator
from leetcode_study_tool.presets import PRESET_MAP


def generate_parser() -> argparse.ArgumentParser:
    """
    Parse the command line arguments.

    Returns
    -------
    argparse.Namespace
        The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Generates problems from LeetCode questions in a desired format."),
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

    input.add_argument(
        "--preset",
        "-p",
        type=str,
        choices=PRESET_MAP.keys(),
        help=("The preset to use to generate problem(s) for."),
    )

    parser.add_argument(
        "--format",
        "-F",
        type=str,
        default="anki",
        choices=["anki", "excel"],
        help="The format to save the Leetcode problem(s) in.",
    )

    parser.add_argument(
        "--template",
        "-t",
        type=str,
        help="Path to a custom Jinja template file for rendering problems.",
    )

    parser.add_argument(
        "--csrf",
        "-c",
        type=str,
        help="The CSRF token to use for LeetCode authentication.",
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
        default="python",
    )

    parser.add_argument(
        "--include-code",
        "-ic",
        action="store_true",
        help="Include solution code from NeetCode GitHub repository using the specified language.",
    )

    return parser


def main():
    parser = generate_parser()
    creator = ProblemsCreator(parser.parse_args())
    creator.create_problems()


if __name__ == "__main__":
    main()
