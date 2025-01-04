import unittest
from datetime import date
from textwrap import dedent
from typing import Any, Dict
import re

import leetcode_study_tool.formatters as formatters
from leetcode_study_tool.queries import get_data, get_url


class TestFormatters(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    def assertAnkiCardStructure(
        self, anki_html: str, problem_slug: str, problem_data: Dict[Any, Any]
    ):
        """
        Instead of comparing exact strings, verify the structure and key components
        of the Anki card HTML.
        """
        self.assertTrue(f"https://leetcode.com/problems/{problem_slug}" in anki_html)

        self.assertTrue(f'<p>{problem_data["difficulty"]}</p>' in anki_html)

        for tag in problem_data["tags"]:
            self.assertTrue(tag["name"] in anki_html)

        self.assertRegex(anki_html, r"<strong>LeetCode User Solutions:</strong>")

        solution_links = re.findall(
            r"https://leetcode\.com/problems/[^/]+/solutions/\d+/1/", anki_html
        )
        self.assertGreater(
            len(solution_links), 0, "Should have at least one solution link"
        )

        if problem_data.get("neetcode_video_id"):
            self.assertTrue("youtube.com/watch?" in anki_html)

    def test_format_list_element(self):
        self.assertEqual(
            dedent(
                formatters.format_list_element("fake-title", ["fake-el-1", "fake-el-2"])
            ),
            dedent(
                """
            <strong>fake-title:</strong><br>
            <ul>
                <li>fake-el-1</li><li>fake-el-2</li>
            </ul>
            """
            ),
        )

    def test_format_solution_link(self):
        self.assertEqual(
            formatters.format_solution_link("fake-slug", "fake-solution-id"),
            "https://leetcode.com/problems/fake-slug/solutions/fake-solution-id/1/",
        )

    def test_format_anki(self):
        """Test the Anki card formatter with actual LeetCode data"""
        problem_slug = "two-sum"
        data = get_data(problem_slug)
        formatted_anki = formatters.format_anki(
            get_url(problem_slug), problem_slug, data
        )

        print(formatted_anki)

        self.assertAnkiCardStructure(formatted_anki, problem_slug, data)

        self.assertTrue(formatted_anki.startswith("    <h1>"))
        self.assertTrue("</ul>" in formatted_anki)

        self.assertEqual(
            formatted_anki.count("<ul>"),
            formatted_anki.count("</ul>"),
            "Mismatched <ul> tags",
        )
        self.assertEqual(
            formatted_anki.count("<li>"),
            formatted_anki.count("</li>"),
            "Mismatched <li> tags",
        )

    def test_format_excel(self):
        data = get_data("two-sum")
        # Don't check the last two elements of the list because they
        # will change over time. Also, mocking time causes issues with
        # urllib, so avoid.
        output = formatters.format_excel(get_url("two-sum"), "two-sum", data)
        output = output[:7]
        self.assertListEqual(
            output,
            [
                "1",
                "Two Sum",
                "Easy",
                "https://leetcode.com/problems/two-sum/",
                date.today(),
                "Array, Hash Table",
                "https://youtube.com/watch?v=KLlXCFG5TnA",
            ],
        )
