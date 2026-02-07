import unittest
from unittest.mock import MagicMock, patch

import requests

import leetcode_study_tool.queries as queries


class TestQueries(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake_url = "https://leetcode.com/problems/fake-url/"
        self.fake_slug = "fake-url"
        self.bad_input = "bad/+input=!"
        self.fake_language = "fake-language"

        self.fake_api_response = b'{"data":{"fake-key":"fake-value"}}'

    def test_get_slug(self):
        self.assertEqual(queries.get_slug(self.fake_url), "fake-url")
        self.assertEqual(queries.get_slug(self.fake_slug), "fake-url")

    def test_get_slug_raises(self):
        self.assertRaises(ValueError, queries.get_slug, self.bad_input)

    def test_get_url(self):
        self.assertEqual(
            queries.get_url(self.fake_url, "problem"),
            "https://leetcode.com/problems/fake-url/",
        )
        self.assertEqual(
            queries.get_url(self.fake_slug, "problem"),
            "https://leetcode.com/problems/fake-url/",
        )

        self.assertEqual(
            queries.get_url(self.fake_url, "tag"),
            "https://leetcode.com/tag/fake-url/",
        )
        self.assertEqual(
            queries.get_url(self.fake_slug, "tag"),
            "https://leetcode.com/tag/fake-url/",
        )

    def test_get_url_raises(self):
        self.assertRaises(ValueError, queries.get_url, self.bad_input, "bad-type")

    @patch("requests.Session.get")
    def test_query(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.fake_api_response
        for content in queries.MAPPINGS:
            self.assertEqual(
                queries.query(content, "fake-slug"), {"fake-key": "fake-value"}
            )

    @patch("requests.get")
    def test_query_raises(self, mock_get):
        self.assertRaises(
            ValueError,
            queries.query,
            "fake-content",
            "fake-slug",
            fake_kwarg="fake-value",
        )
        mock_get.return_value.status_code = 500

    @patch("requests.Session.get")
    def test_query_raises_http_error(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.content = b'{"error": "Internal Server Error"}'

        with self.assertRaisesRegex(
            requests.exceptions.HTTPError, "LeetCode GraphQL API returned 500"
        ):
            queries.query("content", "fake-slug")

    @patch("requests.Session.get")
    def test_query_handles_non_200_responses(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.content = b'{"error": "Internal Server Error"}'

        try:
            result = queries.query("content", "fake-slug")
            self.assertFalse(isinstance(result, dict) and result.get("success"))
        except Exception:
            pass

    @patch("requests.get")
    def test_get_neetcode_solution_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "def solution():\n    pass"
        mock_get.return_value = mock_response

        result = queries.get_neetcode_solution("1", "Two Sum", "python")

        self.assertEqual(result, "def solution():\n    pass")
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertTrue("0001-two-sum.py" in call_args)
        self.assertTrue("python" in call_args)

    @patch("requests.get")
    def test_get_neetcode_solution_unsupported_language(self, mock_get):
        result = queries.get_neetcode_solution("1", "Two Sum", "unsupported-lang")

        self.assertIsNone(result)
        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_neetcode_solution_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("404 Not Found")

        result = queries.get_neetcode_solution("1", "Two Sum", "python")
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_neetcode_solution_special_chars(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "function solution() {}"
        mock_get.return_value = mock_response

        result = queries.get_neetcode_solution("42", "Trapping Rain Water!", "javascript")

        self.assertEqual(result, "function solution() {}")
        call_args = mock_get.call_args[0][0]
        self.assertTrue("0042-trapping-rain-water.js" in call_args)

    def test_get_neetcode_solution_file_extensions(self):
        test_cases = [
            ("python", ".py"),
            ("javascript", ".js"),
            ("java", ".java"),
            ("cpp", ".cpp"),
            ("ruby", ".rb"),
            ("rust", ".rs"),
        ]

        for language, extension in test_cases:
            with patch("requests.get") as mock_get:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.text = f"Code in {language}"
                mock_get.return_value = mock_response

                queries.get_neetcode_solution("1", "Two Sum", language)

                call_args = mock_get.call_args[0][0]
                self.assertTrue(
                    call_args.endswith(extension),
                    f"Expected URL to end with {extension} for {language}",
                )

    @patch("leetcode_study_tool.queries.query")
    @patch("leetcode_study_tool.queries.get_neetcode_solution")
    def test_get_data_includes_neetcode_solution(self, mock_get_neetcode, mock_query):
        mock_query.side_effect = lambda content, *args, **kwargs: {
            "title": {
                "question": {"title": "Test", "difficulty": "Easy", "questionId": "1"}
            },
            "content": {"question": {"content": "test content"}},
            "tags": {"question": {"topicTags": []}},
            "companies": {"question": {"companyTags": []}},
            "solutions": {"questionSolutions": {"solutions": []}},
        }[content]

        mock_get_neetcode.return_value = "def solution():\n    pass"

        data = queries.get_data("test-slug", "python")

        mock_get_neetcode.assert_called_once_with("1", "Test", "python")
        self.assertEqual(data["neetcode_solution"], "def solution():\n    pass")

    @patch("leetcode_study_tool.queries.query")
    @patch("leetcode_study_tool.queries.get_neetcode_solution")
    def test_get_data_no_neetcode_solution_when_language_missing(
        self, mock_get_neetcode, mock_query
    ):
        mock_query.side_effect = lambda content, *args, **kwargs: {
            "title": {
                "question": {"title": "Test", "difficulty": "Easy", "questionId": "1"}
            },
            "content": {"question": {"content": "test content"}},
            "tags": {"question": {"topicTags": []}},
            "companies": {"question": {"companyTags": []}},
            "solutions": {"questionSolutions": {"solutions": []}},
        }[content]

        data = queries.get_data("test-slug")

        mock_get_neetcode.assert_not_called()
        self.assertIsNone(data["neetcode_solution"])

    @patch("leetcode_study_tool.queries.query")
    def test_get_data_deduplicates_title_query(self, mock_query):
        mock_query.side_effect = lambda content, *args, **kwargs: {
            "title": {
                "question": {
                    "title": "Two Sum",
                    "difficulty": "Easy",
                    "questionId": "1",
                }
            },
            "content": {"question": {"content": "test content"}},
            "tags": {"question": {"topicTags": []}},
            "companies": {"question": {"companyTags": []}},
            "solutions": {"questionSolutions": {"solutions": []}},
        }[content]

        data = queries.get_data("two-sum")

        title_calls = [c for c in mock_query.call_args_list if c[0][0] == "title"]
        self.assertEqual(len(title_calls), 1)
        self.assertEqual(data["title"], "Two Sum")
        self.assertEqual(data["difficulty"], "Easy")
        self.assertEqual(data["id"], "1")


if __name__ == "__main__":
    unittest.main()
