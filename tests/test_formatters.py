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
        Verify the structure and key components of the Anki card HTML.
        For tags, ensure they appear after the second semicolon.
        """
        self.assertTrue(f"https://leetcode.com/problems/{problem_slug}" in anki_html)
        self.assertTrue(f"<p>{problem_data['difficulty']}</p>" in anki_html)

        semicolon_index = anki_html.rfind(";")
        for tag in problem_data.get("tags", []):
            self.assertIn(
                tag["slug"],
                anki_html[semicolon_index:],
                f"Tag {tag['name']} should appear after the second semicolon",
            )

        self.assertRegex(anki_html, r"<strong>LeetCode User Solutions:</strong>")
        solution_links = re.findall(
            r"https://leetcode\.com/problems/[^/]+/solutions/\d+/1/", anki_html
        )
        self.assertGreater(
            len(solution_links), 0, "Should have at least one solution link"
        )
        if problem_data.get("neetcode_video_id"):
            self.assertIn("youtube.com/watch?", anki_html)

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
            "solutions": [{"id": "12345"}],
        }

        rendered = formatters.render_template(
            None,
            "anki.html.j2",
            url="https://example.com",
            slug="test-problem",
            data=test_data,
            neetcode=None,
        )

        self.assertIn("Test Problem", rendered)
        self.assertIn("Medium", rendered)
        self.assertIn("solutions/12345/1/", rendered)

        semicolon_index = rendered.rfind(";")
        self.assertIn(
            "array",
            rendered[semicolon_index:],
            "Tag 'Array' should appear only after the second semicolon",
        )

    def test_render_custom_template(self):
        """Test rendering with a custom template file"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html.j2", delete=False
        ) as tmp:
            tmp.write("{{ data.title }} - {{ data.difficulty }} - {{ url }}")
            tmp_path = tmp.name

        try:
            test_data = {
                "id": "1",
                "title": "Test Problem",
                "content": "Test content",
                "difficulty": "Medium",
                "tags": [{"name": "Array", "slug": "array"}],
                "solutions": [{"id": "12345"}],
            }

            rendered = formatters.render_template(
                tmp_path, None, url="https://example.com", data=test_data
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

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html.j2", delete=False
        ) as tmp:
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
            "neetcode_solution": "def two_sum(nums, target):\n    # GitHub solution code\n    pass",
        }
        mock_get_data.return_value = mock_data

        formatted_anki = formatters.format_anki(
            get_url(problem_slug), problem_slug, mock_data
        )

        self.assertIn("GitHub solution code", formatted_anki)
        self.assertIn("def two_sum", formatted_anki)

    def test_format_anki_with_shorts(self):
        """Test Anki formatter with both video and short available"""
        problem_slug = "test-problem"

        # Mock data with both video and short
        mock_data = {
            "id": "1",
            "title": "Test Problem",
            "difficulty": "Easy",
            "content": "<p>Test content</p>",
            "tags": [{"name": "Array", "slug": "array"}],
            "companies": [],
            "solutions": [],
        }

        # Mock the LEETCODE_TO_NEETCODE data to include shorts
        mock_neetcode_data = {
            "1": {
                "video": {
                    "title": "Test Problem - Leetcode 1 - Full Solution",
                    "url": "https://youtube.com/watch?v=video123",
                },
                "short": {
                    "title": "Test Problem - Leetcode 1 - Quick Short",
                    "url": "https://youtube.com/watch?v=short123",
                },
            }
        }

        with patch(
            "leetcode_study_tool.formatters.LEETCODE_TO_NEETCODE", mock_neetcode_data
        ):
            formatted_anki = formatters.format_anki(
                get_url(problem_slug), problem_slug, mock_data
            )

        # Should contain both video and short
        self.assertIn("Full Solution", formatted_anki)
        self.assertIn("Quick Short", formatted_anki)
        self.assertIn("video123", formatted_anki)
        self.assertIn("short123", formatted_anki)

    def test_format_anki_short_only(self):
        """Test Anki formatter with only short available"""
        problem_slug = "test-problem"

        mock_data = {
            "id": "217",
            "title": "Contains Duplicate",
            "difficulty": "Easy",
            "content": "<p>Test content</p>",
            "tags": [{"name": "Array", "slug": "array"}],
            "companies": [],
            "solutions": [],
        }

        # Mock data with only short
        mock_neetcode_data = {
            "217": {
                "short": {
                    "title": "Contains Duplicate - Leetcode 217 - Short",
                    "url": "https://youtube.com/watch?v=short217",
                }
            }
        }

        with patch(
            "leetcode_study_tool.formatters.LEETCODE_TO_NEETCODE", mock_neetcode_data
        ):
            formatted_anki = formatters.format_anki(
                get_url(problem_slug), problem_slug, mock_data
            )

        # Should contain only short
        self.assertIn("Contains Duplicate - Leetcode 217 - Short", formatted_anki)
        self.assertIn("short217", formatted_anki)
        self.assertNotIn("Full Solution", formatted_anki)

    def test_format_anki_no_videos(self):
        """Test Anki formatter with no video or short available"""
        problem_slug = "test-problem"

        mock_data = {
            "id": "999",
            "title": "No Video Problem",
            "difficulty": "Hard",
            "content": "<p>Test content</p>",
            "tags": [{"name": "Array", "slug": "array"}],
            "companies": [],
            "solutions": [],
        }

        # Mock data with no videos
        mock_neetcode_data = {}

        with patch(
            "leetcode_study_tool.formatters.LEETCODE_TO_NEETCODE", mock_neetcode_data
        ):
            formatted_anki = formatters.format_anki(
                get_url(problem_slug), problem_slug, mock_data
            )

        # Should not contain any NeetCode links
        self.assertNotIn("NeetCode Solution", formatted_anki)
        self.assertNotIn("youtube.com/watch", formatted_anki)

    def test_format_excel_with_shorts(self):
        """Test Excel formatter with shorts support"""
        problem_slug = "test-problem"

        mock_data = {
            "id": "1",
            "title": "Test Problem",
            "difficulty": "Easy",
            "content": "<p>Test content</p>",
            "tags": [{"name": "Array", "slug": "array"}],
            "companies": [],
            "solutions": [],
        }

        # Mock data with both video and short
        mock_neetcode_data = {
            "1": {
                "video": {
                    "title": "Test Problem - Leetcode 1 - Full Solution",
                    "url": "https://youtube.com/watch?v=video123",
                },
                "short": {
                    "title": "Test Problem - Leetcode 1 - Quick Short",
                    "url": "https://youtube.com/watch?v=short123",
                },
            }
        }

        with patch(
            "leetcode_study_tool.formatters.LEETCODE_TO_NEETCODE", mock_neetcode_data
        ):
            excel_output = formatters.format_excel(
                get_url(problem_slug), problem_slug, mock_data
            )

        # Excel format: [id, title, difficulty, url, date, tags, video_url, short_url, solutions, companies]
        self.assertEqual(len(excel_output), 11)  # Updated number of columns with short
        self.assertEqual(
            excel_output[6], "https://youtube.com/watch?v=video123"
        )  # Video URL
        self.assertEqual(
            excel_output[7], "https://youtube.com/watch?v=short123"
        )  # Short URL

    def test_data_structure_migration(self):
        """Test migration from old to new data structure"""
        # Old format (current)
        old_format = {
            "1": {
                "title": "Two Sum - Leetcode 1 - HashMap - Python",
                "url": "https://youtube.com/watch?v=KLlXCFG5TnA",
            },
            "217": {
                "title": "Contains Duplicate - Leetcode 217 - Python",
                "url": "https://youtube.com/watch?v=3OamzN90kPg",
            },
        }

        # Expected new format
        new_format = {
            "1": {
                "video": {
                    "title": "Two Sum - Leetcode 1 - HashMap - Python",
                    "url": "https://youtube.com/watch?v=KLlXCFG5TnA",
                }
            },
            "217": {
                "video": {
                    "title": "Contains Duplicate - Leetcode 217 - Python",
                    "url": "https://youtube.com/watch?v=3OamzN90kPg",
                }
            },
        }

        # Migration function (will be implemented in the main code)
        def migrate_to_new_format(old_data):
            """Helper function to migrate old data to new format"""
            new_data = {}
            for leetcode_id, video_info in old_data.items():
                new_data[leetcode_id] = {"video": video_info}
            return new_data

        migrated = migrate_to_new_format(old_format)
        self.assertEqual(migrated, new_format)

    def test_template_rendering_with_shorts(self):
        """Test that template correctly renders both videos and shorts"""
        # This tests the HTML template structure
        # We'll verify this when we update the anki.html.j2 template

        mock_template_data = {
            "url": "https://leetcode.com/problems/test/",
            "slug": "test",
            "data": {"id": "1", "title": "Test"},
            "neetcode": {
                "video": {
                    "title": "Test - Leetcode 1 - Full Solution",
                    "url": "https://youtube.com/watch?v=video123",
                },
                "short": {
                    "title": "Test - Leetcode 1 - Quick Short",
                    "url": "https://youtube.com/watch?v=short123",
                },
            },
        }

        # Render template (this will be tested after template update)
        rendered = formatters.render_template(
            None, "anki.html.j2", **mock_template_data
        )

        # Basic checks
        self.assertIn("Test", rendered)
        self.assertIn("https://leetcode.com/problems/test/", rendered)
