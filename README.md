# Leetcode Study Tool
![Tests Status](https://github.com/johnsutor/leetcode-study-tool/workflows/Tests/badge.svg)
![Style Status](https://github.com/johnsutor/leetcode-study-tool/workflows/Style/badge.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
[![PyPi](https://img.shields.io/pypi/v/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat)

This package lets you get grokking as quickly as possible with Leetcode. It provides a command-line tool for interracting with Leetcode to create either an Excel file or Anki flashcards for study. Currently, this tool supports taking in a list of leetcode question slugs or URLs or popular study sets (including the [Blind 75](https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU), [Grind 75](https://www.techinterviewhandbook.org/grind75), and [Neetcode 150](https://neetcode.io/practice)). 

## Why? 
This package was created as an opinionated alternative to other existing packages (as listed at the bottom of this README). 

## Installation
```shell
$ pip install leetcode-study-tool
```

## Usage 
```shell
usage: leetcode-study-tool [-h]
                           (--url URL | --file FILE | --preset {blind_75,grind_75,grind_169,neetcode_150,neetcode_all})
                           [--format {anki,excel}] [--csrf CSRF] [--output OUTPUT]
                           [--language LANGUAGE]

Generates problems from LeetCode questions in a desired format.

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     The URL(s) or slug(s) of the LeetCode question(s) to generate
                        problem(s) for. (default: None)
  --file FILE, -f FILE  The file containing the URL(s) or slug(s) of the LeetCode question(s)
                        to generate problem(s) for. (default: None)
  --preset {blind_75,grind_75,grind_169,neetcode_150,neetcode_all}, -p {blind_75,grind_75,grind_169,neetcode_150,neetcode_all}
                        The preset to use to generate problem(s) for. (default: None)
  --format {anki,excel}, -F {anki,excel}
                        The format to save the Leetcode problem(s) in. (default: anki)
  --csrf CSRF, -c CSRF  The CSRF token to use for LeetCode authentication. (default: None)
  --output OUTPUT, -o OUTPUT
                        The output file to write the problem(s) to. (default: output.txt)
  --language LANGUAGE, -l LANGUAGE
                        The language to generate problem(s) for. (default: None)
```

## Example 
In the simplest case, if you want to [Grok](https://www.reddit.com/r/leetcode/comments/t5xqb6/how_to_use_grokking/) the most commonly asked questions, you should generate from a preset. For example, generating Anki cards from the [Grind 75](https://www.techinterviewhandbook.org/grind75) is as simple as 
```shell
$ leetcode-study-tool -p grind_75
```
Perhaps, instead, you'd prefer to import questions that you've already worked on. In a directory with a file named `questions.txt`, where each line is either a Leetcode problem URL or slug (or a combination of both), we can run the command 
```shell
$ leetcode-study-tool -f questions.txt 
```
which will generate the file `output.txt`. We can then open Anki to import these problems as demonstrated below, *ensuring to select semicolon as a field separator*.

![anki demo](static/anki-demo.gif)

## Anki
When generating an Anki output, the resulting "cards" are saved as a `.txt` file. These cards include three fields:
1. The front of the study card, containing the question ID, Title, URL, and problem description 
2. The publicly available solutions (and NeetCode solution, if available)
3. The tags associated with the problem (i.e., if the problem involves a hash map, arrays, etc...)

## Excel
When generating an Excel output, the resulting questions are saved in an `.xlsx` file. Each problem includes the following fields:
1. ID of the leetcode question
2. Title of the leetcode question
3. URL of the leetcode question
4. Last date that this question was attempted by the user (please note that this is not pulled from your leetcode profile, but left for you to update as you progress in solving leetcode questions)
5. The tags associated with the problem (i.e., if the problem involves a hash map, arrays, etc...)
6. Neetcode video link (if it exists)
7. Solution links for the problem (if they are reachable)
8. Companies that have asked this question recently in interviews (if they are reachable)

## Roadmap 
- [X] Use TQDM to show card generation progress
- [X] Add support for exporting to an excel sheet
- [X] Add support for showing neetcode solutions on the back of the card as a 
- [ ] Add support for getting the difficulty of questions 
- [ ] Add support for fetching premium questions via authentification
- [ ] Add support for importing cards into Quizlet
- [ ] Add support for fetching questions by topic or tag 
link
- [ ] Allow for the definition of custom formatters and outputs (including which fields are included or excluded)
- [ ] Reach 90% test coverage

## Other Usefull Stuff
- [Remember anything with Anki](https://foggymountainpass.com/anki-essentials/)
- [Leetcode Anki Card Generator](https://github.com/fspv/leetcode-anki)
- [Leetcode API](https://github.com/fspv/python-leetcode)
