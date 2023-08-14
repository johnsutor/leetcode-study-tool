#!/usr/bin/env python
# encoding: utf-8
# Utility script to generate lists of presets for the leetcode_study_tool. This includes
# the Blind 75, the Grind 75, and the Grind 169.

import json
import sys
import urllib

import requests
from bs4 import BeautifulSoup


def main(url: str, output_file: str = "presets.txt"):
    response = requests.get(url)
    problems = []

    soup = BeautifulSoup(response.content, "html.parser")

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

    with open(output_file, "w") as f:
        json.dump(problems, f)


if __name__ == "__main__":
    url = sys.argv[1]
    if sys.argv[2]:
        output_file = sys.argv[2]
    else:
        output_file = "presets.txt"
    main(url, output_file)
