# Leetcode Study Tool
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

This package provides a command-line tool for interracting with Leetcode to create flashcards for study,
which can then be imported into Anki.

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

## Roadmap 
- [ ] Add support for fetching premium questions via authentification
- [ ] Add support for importing cards into Quizlet
- [ ] Add support for fetching questions by topic or tag 
- [ ] Add support for exporting to an excel sheet
- [ ] Add support for showing neetcode solutions on the back of the card as a link
- [ ] Reach 100% test coverage