#!/usr/bin/env python
# encoding: utf-8
# Utility script to generate lists of presets for the leetcode_study_tool. This includes
# the Blind 75, the Grind 75, and the Grind 169.

import argparse
import json
import urllib

import requests
from bs4 import BeautifulSoup


def main(args: argparse.Namespace):
    if args.url:
        response = requests.get(args.url)
        html = response.content
    else:
        with open(args.file, "r") as f:
            html = f.read()

    problems = []

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a"):
        # save only the links that are leetcode problems
        url = urllib.parse.urlparse(link.get("href"))

        try:
            if (
                url.path.startswith("/problems/")
                and url.netloc == "leetcode.com"
            ):
                problems.append(url.geturl())
        except Exception as e:
            print(e)
            if (
                url.path.decode().startswith("/problems/")
                and url.netloc.decode() == "leetcode.com"
            ):
                problems.append(url.geturl().decode())

    with open(args.output, "a") as f:
        json.dump(problems, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    input_type = parser.add_mutually_exclusive_group(
        required=True,
    )
    input_type.add_argument(
        "--url",
        help="URL of the leetcode list to scrape",
        type=str,
    )

    input_type.add_argument(
        "--file",
        help="HTML File containing the list of leetcode problems",
        type=str,
    )

    parser.add_argument(
        "--output",
        help="Output file to write to",
        type=str,
        default="presets.txt",
    )

    args = parser.parse_args()
    main(args)
