# 💻 Leetcode Study Tool
![Tests Status](https://github.com/johnsutor/leetcode-study-tool/workflows/Tests/badge.svg)
![Style Status](https://github.com/johnsutor/leetcode-study-tool/workflows/Style/badge.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
[![PyPi](https://img.shields.io/pypi/v/leetcode-study-tool)](https://pypi.org/project/leetcode-study-tool/)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat)

![Leetcode Study Tool Diagram](https://github.com/johnsutor/leetcode-study-tool/raw/main/static/leetcode_study_tool_diagram.png)

This package lets you get grokking as quickly as possible with Leetcode. It provides a command-line tool for interracting with Leetcode to create either an Excel file or Anki flashcards for study. Currently, this tool supports taking in a list of leetcode question slugs or URLs or popular study sets (including the [Blind 75](https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU), [Grind 75](https://www.techinterviewhandbook.org/grind75), and [Neetcode 150](https://neetcode.io/practice)). 

## 🤔 Why? 
This package was created as an opinionated alternative to other existing packages (as listed at the bottom of this README). 

## 📥 Installation
```shell
$ pip install leetcode-study-tool
```

## 💻 Usage 
```shell
usage: leetcode-study-tool [-h] (--url URL | --file FILE | --preset {blind_75,grind_75,grind_169,neetcode_150,neetcode_250,neetcode_all}) [--format {anki,excel}]
                           [--template TEMPLATE] [--csrf CSRF] [--output OUTPUT] [--language LANGUAGE] [--include-code]

Generates problems from LeetCode questions in a desired format.

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     The URL(s) or slug(s) of the LeetCode question(s) to generate problem(s) for. (default: None)
  --file FILE, -f FILE  The file containing the URL(s) or slug(s) of the LeetCode question(s) to generate problem(s) for. (default: None)
  --preset {blind_75,grind_75,grind_169,neetcode_150,neetcode_250,neetcode_all}, -p {blind_75,grind_75,grind_169,neetcode_150,neetcode_250,neetcode_all}
                        The preset to use to generate problem(s) for. (default: None)
  --format {anki,excel}, -F {anki,excel}
                        The format to save the Leetcode problem(s) in. (default: anki)
  --template TEMPLATE, -t TEMPLATE
                        Path to a custom Jinja template file for rendering problems. (default: None)
  --csrf CSRF, -c CSRF  The CSRF token to use for LeetCode authentication. (default: None)
  --output OUTPUT, -o OUTPUT
                        The output file to write the problem(s) to. (default: output.txt)
  --language LANGUAGE, -l LANGUAGE
                        The language to generate problem(s) for. (default: None)
  --include-code, -ic   Include solution code from NeetCode GitHub repository using the specified language. (default: False)
```

## 💡 Example 
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

### Including Solution Code

You can include solution code from the NeetCode GitHub repository by using the `--include-code` flag along with specifying a programming language:

```shell
$ leetcode-study-tool -p grind_75 --language python --include-code
```

This will fetch solution code in the specified language (when available) and include it in your Anki cards or Excel output.

Supported languages include: c, cpp, csharp, dart, go, java, javascript, kotlin, python, ruby, rust, scala, swift, and typescript.

## 📒 Anki
When generating an Anki output, the resulting "cards" are saved as a `.txt` file. These cards include three fields:
1. The front of the study card, containing the question ID, Title, URL, and problem description 
2. The publicly available solutions (and NeetCode solution or code, if available)
3. The tags associated with the problem (i.e., if the problem involves a hash map, arrays, etc...)

## 📊 Excel
When generating an Excel output, the resulting questions are saved in an `.xlsx` file. Each problem includes the following fields:
1. ID of the leetcode question
2. Title of the leetcode question
3. URL of the leetcode question
4. Last date that this question was attempted by the user (please note that this is not pulled from your leetcode profile, but left for you to update as you progress in solving leetcode questions)
5. The tags associated with the problem (i.e., if the problem involves a hash map, arrays, etc...)
6. Neetcode video link (if it exists)
7. Solution links for the problem (if they are reachable)
8. Companies that have asked this question recently in interviews (if they are reachable)

## Custom Templates

LeetCode Study Tool supports custom Jinja2 templates for generating Anki cards or other outputs. You can specify your own template file using the `--template` flag:

```bash
leetcode-study-tool --url "https://leetcode.com/problems/two-sum/" --template "path/to/my_template.jinja"
```

### Template Variables

When creating your custom template, the following variables are available:

| Variable | Description |
|----------|-------------|
| `url` | The URL to the LeetCode problem |
| `slug` | The problem slug |
| `data` | Object containing all problem data |
| `data.id` | Problem ID |
| `data.title` | Problem title |
| `data.content` | Problem description (HTML) |
| `data.difficulty` | Problem difficulty (Easy, Medium, Hard) |
| `data.tags` | List of topic tags for the problem |
| `data.companies` | List of companies that ask this problem |
| `data.solutions` | List of available solutions on LeetCode |
| `data.neetcode_solution` | NeetCode solution code (if --include-code is used) |
| `data.language` | Language of the solution code |
| `neetcode` | NeetCode video information (when available) |

### Solution Code Example

Here's an example template that highlights the solution code:

```jinja
<h1>{{ data.id }}. {{ data.title }} ({{ data.difficulty }})</h1>

<div class="content">
  {{ data.content }}
</div>

<div class="tags">
  {% for tag in data.tags %}
    <span class="tag">{{ tag.name }}</span>
  {% endfor %}
</div>

;

{% if data.neetcode_solution %}
<h3>Solution Code ({{ data.language }})</h3>
<pre><code>
{{ data.neetcode_solution }}
</code></pre>
{% endif %}

{% if data.solutions %}
<div class="community-solutions">
  <h3>Community Solutions:</h3>
  <ul>
    {% for solution in data.solutions[:3] %}
      <li><a href="{{ solution_url(slug, solution.id) }}">Solution {{ loop.index }}</a></li>
    {% endfor %}
  </ul>
</div>
{% endif %}

;

{{ data.tags|map(attribute='slug')|join(' ') }}
```

## 🛠 Development 

For developers who want to contribute to this project, we use UV for dependency management:

### Setup with UV
```shell
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the project
git clone https://github.com/johnsutor/leetcode-study-tool.git
cd leetcode-study-tool
uv sync --dev
```

### Development Commands
```shell
# Format code
make format

# Check formatting
make format-check

# Run tests
make test

# Type checking
make type-check

# Sync dependencies
make sync

# Install only main dependencies
make install
```

### Using UV Directly
```shell
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Run any command in the project environment
uv run python leetcode_study_tool/cli.py --help

# Update lockfile
uv lock
```

## 🛣 Roadmap 
- [X] Use TQDM to show card generation progress
- [X] Add support for exporting to an excel sheet
- [X] Add support for showing neetcode solutions on the back of the card as a 
- [X] Add support for getting the difficulty of questions 
- [X] Add support for Jinja templating formatters 
- [X] Add support for including NeetCode solution code
- [X] Migrate to UV for faster dependency management
- [X] Add NeetCode shorts 
- [ ] Add support for fetching premium questions via authentification
- [ ] Add support for importing cards into Quizlet
- [ ] Add support for fetching questions by topic or tag 
link
- [ ] Reach 90% test coverage

## 🔎 Other Usefull Stuff
- [Remember anything with Anki](https://foggymountainpass.com/anki-essentials/)
- [Leetcode Anki Card Generator](https://github.com/fspv/leetcode-anki)
- [Leetcode API](https://github.com/fspv/python-leetcode)
