import json
import re
from functools import lru_cache
from typing import Union
from urllib.parse import urlparse

import requests

from .constants.graphql import (
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
        The type of the URL to get. Defaults to 'question', must be one of 'question' or 'tag'.

    Returns
    -------
    str
        The URL of the given slug or URL.

    Raises
    ------
    ValueError
        If the given type is not one of 'question' or 'tag', or if the input is not a valid slug or URL.
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


@lru_cache(maxsize=None)
def query(content: str, slug: str, **kwargs) -> dict:
    """
    Query the LeetCode GraphQL API for the given content.

    Arguments
    ---------
    content : str
        The content to query for.
    slug : str
        The slug of the question to query for.
    **kwargs
        Any additional arguments to pass to the query.

    Returns
    -------
    dict
        The response from the LeetCode GraphQL API.

    Raises
    ------
    requests.exceptions.HTTPError
        If the response from the LeetCode GraphQL API is not 200.
    """
    assert content in MAPPINGS.keys(), f"Invalid query content: {content}"
    response = requests.get(
        url=BASE_URL,
        json={
            "query": MAPPINGS[content],
            "variables": {"titleSlug": slug, **kwargs},
        },
    )
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8")).get("data")
    else:
        raise requests.exceptions.HTTPError(
            f"LeetCode GraphQL API returned {response.status_code}"
        )


def get_data(slug: str, language: Union[str, None] = None) -> dict:
    """
    Get the relevant data for constructing the Anki card for the given URL.

    Arguments
    ---------
    slug : str
        The slug of the question to generate an Anki card for.
    language : str
        The language to generate an Anki card for.

    Returns
    -------
    dict
        The relevant data for constructing the Anki card for the given URL.
    """
    title = query("title", slug)["question"]["title"]
    content = query("content", slug)["question"]["content"]
    id = query("title", slug)["question"]["questionId"]
    tags = query("tags", slug)["question"]["topicTags"]
    companies = query("companies", slug)["question"]["companyTags"]
    solutions = query(
        "solutions", slug, skip=0, first=10, languageTags=(language)
    )["questionSolutions"]["solutions"]

    results = {
        "title": title,
        "content": content,
        "id": id,
        "tags": tags,
        "companies": companies,
        "solutions": solutions,
    }

    return results
