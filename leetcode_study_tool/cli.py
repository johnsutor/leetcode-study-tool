import argparse

from leetcode_study_tool.creator import ProblemsCreator


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
        default="anki",
        choices=["anki"],
        help="The format to save the Leetcode problem(s) in.",
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
    )

    return parser.parse_args()


def main():
    args = parse_args()
    creator = ProblemsCreator(args)
    creator.create_problems()


if __name__ == "__main__":
    main()
