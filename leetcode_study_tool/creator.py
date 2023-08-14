import argparse
import html
import os
import re
from functools import partial
from multiprocessing import Pool
from typing import List, Union

from .formatters import FORMAT_MAP
from .outputs import SAVE_MAP
from .queries import generate_session, get_data, get_slug


class ProblemsCreator:
    """
    Create problems for Anki from the CLI inputs.
    """

    def __init__(self, args: Union[argparse.Namespace, dict]) -> None:
        # Explicitly define for linting
        self.format = "anki"
        self.output = "output"

        args = vars(args)
        for key in args:
            setattr(self, key, args[key])

        if args.get("language"):
            self.language = args["language"].strip().lower()
        else:
            self.language = None

        if args.get("csrf"):
            self.session = generate_session(args["csrf"])
        else:
            self.session = generate_session()

        if args.get("url"):
            self.urls = args["url"].split(",")

        elif args.get("file"):
            with open(args["file"], "r") as f:
                self.urls = f.read().splitlines()

    def create_problems(self) -> None:
        """
        Create the problems for Anki.
        """
        with Pool() as pool:
            problems = pool.map(
                partial(
                    self._generate_problem,
                    language=self.language,
                    format=self.format,
                ),
                self.urls,
            )

        self._save_output(problems, self.output)

    def _sanitize(self, input: Union[str, list, None]) -> Union[str, list]:
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

    def _save_output(self, problems: List[Union[str, None]], file: str) -> None:
        file_name = os.path.splitext(os.path.basename(file))[0]

        SAVE_MAP[self.format](problems, file_name)

    def _generate_problem(self, url: str) -> Union[str, None]:
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
        try:
            data = get_data(slug, self.language, self.session)
        except Exception as e:
            print(f"Failed to generate problem for {url}: {e}")
            return None

        data = {k: self._sanitize(v) for k, v in data.items()}

        return FORMAT_MAP[self.format](url, slug, data)
