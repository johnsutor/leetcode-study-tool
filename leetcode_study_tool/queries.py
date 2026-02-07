import json
import re
from typing import Optional, Union
from urllib.parse import urlparse

import requests

from leetcode_study_tool.graphql import (
    BASE_URL,
    COMMUNITY_SOLUTIONS,
    QUESTION_CONTENT,
    QUESTION_DETAIL_COMPANY_TAGS,
    QUESTION_TITLE,
    SINGLE_QUESTION_TOPIC_TAGS,
)

MAPPINGS = {
    "content": QUESTION_CONTENT,
    "title": QUESTION_TITLE,
    "tags": SINGLE_QUESTION_TOPIC_TAGS,
    "companies": QUESTION_DETAIL_COMPANY_TAGS,
    "solutions": COMMUNITY_SOLUTIONS,
}

NEETCODE_LANGUAGES = [
    "c",
    "cpp",
    "csharp",
    "dart",
    "go",
    "java",
    "javascript",
    "kotlin",
    "python",
    "ruby",
    "rust",
    "scala",
    "swift",
    "typescript",
]
NEETCODE_BASE_URL = (
    "https://raw.githubusercontent.com/neetcode-gh/leetcode/refs/heads/main"
)

NEETCODE_EXTENSIONS = {
    "c": ".c",
    "cpp": ".cpp",
    "csharp": ".cs",
    "dart": ".dart",
    "go": ".go",
    "java": ".java",
    "javascript": ".js",
    "kotlin": ".kt",
    "python": ".py",
    "ruby": ".rb",
    "rust": ".rs",
    "scala": ".scala",
    "swift": ".swift",
    "typescript": ".ts",
}


def get_slug(input: str) -> str:
    """
    Get the question slug from the given input, whether it's a URL or slug.

    Arguments
    ---------
    input : str
        The URL or slug of the question to get the slug of.

    Returns
    -------
    str
        The slug of the given URL or slug.
    """
    url = urlparse(input)

    if url.scheme and url.netloc:
        return url.path.split("/")[2]
    elif re.match(r"^[a-z0-9\-]+$", input):
        return input
    else:
        raise ValueError(f"Invalid input: {input}")


def get_url(input: str, type: str = "problem") -> str:
    """
    Get the question URL from the given input, whether it's a URL or slug.

    Arguments
    ---------
    input : str
        The URL or slug of the question to get the url of.
    type: str
        The type of the URL to get. Defaults to 'problem', must be one of
        'problem' or 'tag'.

    Returns
    -------
    str
        The URL of the given slug or URL.

    Raises
    ------
    ValueError
        If the given type is not one of 'problem' or 'tag', or if the input
        is not a valid slug or URL.
    """
    url = urlparse(input)
    if type not in ["problem", "tag"]:
        raise ValueError(f"Invalid type: {type}")

    if url.scheme and url.netloc:
        input = get_slug(input)
    if type == "problem":
        return f"https://leetcode.com/problems/{input}/"
    else:
        return f"https://leetcode.com/tag/{input}/"


def generate_session(csrf_token: Union[str, None] = None) -> requests.Session:
    """
    Generate a requests session with the LeetCode GraphQL API.

    Arguments
    ---------
    csrf_token : Union[str, None]
        The CSRF token to use for the session.

    Returns
    -------
    requests.Session
        A requests session with the LeetCode GraphQL API.
    """
    session = requests.Session()

    if csrf_token:
        session.headers.update({"X-Csrftoken": csrf_token})

    return session


def query(
    content: str,
    slug: str,
    session: Union[requests.Session, None] = None,
    **kwargs,
) -> dict:
    """
    Query the LeetCode GraphQL API for the given content.

    Arguments
    ---------
    content : str
        The content to query for.
    slug : str
        The slug of the question to query for.
    session : Union[requests.Session, None]
        The requests session to use. If None, a new session is created.
    **kwargs
        Any additional arguments to pass to the query.

    Returns
    -------
    dict
        The response from the LeetCode GraphQL API.

    Raises
    ------
    ValueError
        If the content is not a valid query type.
    requests.exceptions.HTTPError
        If the response from the LeetCode GraphQL API is not 200.
    """
    if content not in MAPPINGS:
        raise ValueError(f"Invalid query content: {content}")

    if not session:
        session = generate_session()

    response = session.get(
        url=BASE_URL,
        json={
            "query": MAPPINGS[content],
            "variables": {"titleSlug": slug, **kwargs},
        },
    )

    if response.status_code == 200:
        return dict(json.loads(response.content.decode("utf-8")).get("data"))

    raise requests.exceptions.HTTPError(
        f"LeetCode GraphQL API returned {response.status_code}",
        response=response,
    )


def get_neetcode_solution(
    problem_id: str, title: str, language: str = "python"
) -> Optional[str]:
    """
    Get the solution for a given problem from the NeetCode GitHub repository.

    Arguments
    ---------
    problem_id : str
        The ID of the problem to get the solution for.
    title : str
        The title of the problem to get the solution for.
    language : str
        The language to get the solution for. Must be one of the supported
        languages. Defaults to 'python'.

    Returns
    -------
    Optional[str]
        The solution code if found, None otherwise.
    """
    if language not in NEETCODE_LANGUAGES:
        return None

    padded_id = problem_id.zfill(4)
    kebab_title = re.sub(r"[^a-zA-Z0-9\s]", "", title).lower().replace(" ", "-")
    file_name = f"{padded_id}-{kebab_title}"
    ext = NEETCODE_EXTENSIONS.get(language, "")
    url = f"{NEETCODE_BASE_URL}/{language}/{file_name}{ext}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None


def get_data(
    slug: str,
    language: Union[str, None] = None,
    session: Union[requests.Session, None] = None,
) -> dict:
    """
    Get the relevant data for constructing a study card for the given slug.

    Arguments
    ---------
    slug : str
        The slug of the question to get data for.
    language : Union[str, None]
        The language to get solutions for.
    session : Union[requests.Session, None]
        The requests session to use.

    Returns
    -------
    dict
        The relevant data for constructing the study card.
    """
    if not session:
        session = generate_session()

    title_data = query("title", slug, session)["question"]
    title = title_data["title"]
    difficulty = title_data["difficulty"]
    question_id = title_data["questionId"]

    content = query("content", slug, session)["question"]["content"]
    tags = query("tags", slug, session)["question"]["topicTags"]
    companies = query("companies", slug, session)["question"]["companyTags"]
    solutions = query(
        "solutions", slug, session, skip=0, first=10, languageTags=(language)
    )["questionSolutions"]["solutions"]

    neetcode_solution = None
    if language:
        neetcode_solution = get_neetcode_solution(question_id, title, language)

    return {
        "title": title,
        "content": content,
        "difficulty": difficulty,
        "id": question_id,
        "tags": tags,
        "companies": companies,
        "solutions": solutions,
        "neetcode_solution": neetcode_solution,
    }
