# Leetcode Study Tool
![Tests Status](https://github.com/johnsutor/leetcode-study-tool/workflows/Tests/badge.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
[![PyPi](https://img.shields.io/pypi/v/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat)

This package provides a command-line tool for interracting with Leetcode to create flashcards for study,
which can then be imported into Anki. Currently, this tool supports taking in a list of URLs and outputting 
problems in a format that can be imported to Anki. These cards include three fields:
1. The front of the study card, containing the question ID, Title, URL, and problem description 
2. The publicly available solutions (and NeetCode solution, if available)
3. The tags associated with the problem (i.e., if the problem involves a hash map, arrays, etc...)

## Installation
```shell
$ pip install leetcode-study-tool
```

## Usage 
```shell
usage: leetcode-study-tool [-h] (--url URL | --file FILE) [--format {cards}] [--output OUTPUT] [--language LANGUAGE]

Generates problems from LeetCode questions in a desired format.

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     The URL(s) or slug(s) of the LeetCode question(s) to generate problem(s) for. (default: None)
  --file FILE, -f FILE  The file containing the URL(s) or slug(s) of the LeetCode question(s) to generate problem(s) for. (default: None)
  --format {cards}, -F {cards}
                        The format to save the Anki problem(s) in. (default: cards)
  --output OUTPUT, -o OUTPUT
                        The output file to write the problem(s) to. (default: output.txt)
  --language LANGUAGE, -l LANGUAGE
                        The language to generate problem(s) for. (default: None)
```

## Example 
In a directory with a file named `questions.txt`, where each line is either a Leetcode problem URL or slug (or a combination of both), we can run the command 
```shell
$ leetcode-study-tool -f questions.txt 
```
which will generate the file `output.txt`. We can then open Anki to import these problems as demonstrated below, *ensuring to select semicolon as a field separator*.

![anki demo](static/anki-demo.gif)


## Roadmap 
- [ ] Add support for fetching premium questions via authentification
- [ ] Add support for importing cards into Quizlet
- [ ] Add support for fetching questions by topic or tag 
- [ ] Add support for exporting to an excel sheet
- [ ] Add support for showing neetcode solutions on the back of the card as a link
- [ ] Reach 100% test coverage