import unittest
from datetime import date
from textwrap import dedent
from typing import Any, Dict
import re
import tempfile
import os
from unittest.mock import patch

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

        self.assertTrue(formatted_anki.startswith("<h1>"))  
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

    def test_render_template(self):
        """Test the template rendering functionality"""
        test_data = {
            "id": "1",
            "title": "Test Problem",
            "content": "Test content",
            "difficulty": "Medium",
            "tags": [{"name": "Array", "slug": "array"}],
            "solutions": [{"id": "12345"}]
        }
        
        rendered = formatters.render_template(
            None, 
            "anki.html.j2", 
            url="https://example.com",
            slug="test-problem",
            data=test_data,
            neetcode=None
        )
        
        self.assertIn("Test Problem", rendered)
        self.assertIn("Array", rendered)
        self.assertIn("Medium", rendered)
        self.assertIn("solutions/12345/1/", rendered)

    def test_render_custom_template(self):
        """Test rendering with a custom template file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html.j2', delete=False) as tmp:
            tmp.write("{{ data.title }} - {{ data.difficulty }} - {{ url }}")
            tmp_path = tmp.name
        
        try:
            test_data = {
                "id": "1",
                "title": "Test Problem",
                "content": "Test content",
                "difficulty": "Medium",
                "tags": [{"name": "Array", "slug": "array"}],
                "solutions": [{"id": "12345"}]
            }
            
            rendered = formatters.render_template(
                tmp_path,  
                None,     
                url="https://example.com",
                data=test_data
            )
            
            self.assertEqual("Test Problem - Medium - https://example.com", rendered)
        finally:
            os.unlink(tmp_path)

    def test_render_template_error(self):
        """Test error handling when no template is provided"""
        with self.assertRaises(ValueError):
            formatters.render_template(None, None)

    def test_format_anki_custom_template(self):
        """Test the Anki card formatter with custom template"""
        problem_slug = "two-sum"
        data = get_data(problem_slug)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html.j2', delete=False) as tmp:
            tmp.write("CUSTOM: {{ data.title }} - {{ data.difficulty }} - {{ url }}")
            tmp_path = tmp.name
        
        try:
            formatted_anki = formatters.format_anki(
                get_url(problem_slug), problem_slug, data, template_path=tmp_path
            )
            
            self.assertIn("CUSTOM:", formatted_anki)
            self.assertIn("Two Sum", formatted_anki)
            self.assertIn("Easy", formatted_anki)
        finally:
            os.unlink(tmp_path)

    def test_format_anki_with_template(self):
        """Test the Anki card formatter with templates"""
        problem_slug = "two-sum"
        data = get_data(problem_slug)
        formatted_anki = formatters.format_anki(
            get_url(problem_slug), problem_slug, data
        )

        self.assertIn("<h1>", formatted_anki)
        self.assertIn("</h1>", formatted_anki)
        
        if data.get("companies"):
            self.assertIn("Companies:", formatted_anki)
        
        if str(data["id"]) in formatters.LEETCODE_TO_NEETCODE:
            self.assertIn("NeetCode Solution:", formatted_anki)

    @patch("leetcode_study_tool.queries.get_data")
    def test_format_anki_with_github_solution(self, mock_get_data):
        """Test the Anki card formatter with a GitHub solution"""
        problem_slug = "two-sum"
        
        mock_data = {
            "id": "1",
            "title": "Two Sum",
            "difficulty": "Easy",
            "content": "<p>Test content</p>",
            "tags": [{"name": "Array", "slug": "array"}],
            "companies": [{"name": "Amazon", "slug": "amazon"}],
            "solutions": [{"id": "12345"}],
            "neetcode_solution": "def two_sum(nums, target):\n    # GitHub solution code\n    pass"
        }
        mock_get_data.return_value = mock_data
        
        formatted_anki = formatters.format_anki(
            get_url(problem_slug), problem_slug, mock_data
        )
        
        self.assertIn("GitHub solution code", formatted_anki)
        self.assertIn("def two_sum", formatted_anki)
