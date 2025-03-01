import argparse
import unittest
from unittest.mock import MagicMock, patch

import leetcode_study_tool.creator as creator


class TestCreator(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake_string_to_sanitize = (
            "<strong>fake&lt;string&nbsp;to&gt;sanitize</strong>\n<p> More;"
            " content to sanitize </p><br><br><br><br>"
        )
        self.fake_parsed_args_file = argparse.Namespace(
            url=None,
            file="fake-file",
            output="fake-output",
            format="anki",
            language=None,
            include_code=False, 
        )
        self.fake_parsed_args_url = argparse.Namespace(
            file=None,
            url="fake-url-one,fake-url-two,fake-url-three",
            output="fake-output",
            format="anki",
            language=None,
            include_code=False,  
        )
        self.fake_parsed_args_with_code = argparse.Namespace(
            file=None,
            url="fake-url",
            output="fake-output",
            format="anki",
            language="python",
            include_code=True,  
        )

    @patch("builtins.open")
    def test_sanitize(self, mock_open):
        mock_problem_creator = creator.ProblemsCreator(self.fake_parsed_args_file)
        self.assertEqual(
            mock_problem_creator._sanitize(self.fake_string_to_sanitize),
            "<strong>fake<string\xa0to>sanitize</strong><br> <p> More  content"
            " to sanitize </p><br>",
        )

    @patch("builtins.open")
    def test_save_output_string(self, mock_save_string):
        mock_save_string = MagicMock()
        with patch.dict(
            "leetcode_study_tool.outputs.SAVE_MAP", {"anki": mock_save_string}
        ):
            mock_problem_creator = creator.ProblemsCreator(self.fake_parsed_args_file)
            mock_problem_creator._save_output(
                ["fake-problem-one", "fake-problem-two"], "fake-output"
            )
            mock_save_string.assert_called_once_with(
                ["fake-problem-one", "fake-problem-two"], "fake-output"
            )

    @patch("builtins.open")
    def test_generate_problem(self, mock_open):
        mock_format_anki = MagicMock()
        with patch.dict(
            "leetcode_study_tool.formatters.FORMAT_MAP",
            {"anki": mock_format_anki},
        ):
            mock_problem_creator = creator.ProblemsCreator(self.fake_parsed_args_file)
            mock_problem_creator._generate_problem("two-sum")
            mock_format_anki.assert_called_once()

    @patch("leetcode_study_tool.creator.get_data")
    @patch("leetcode_study_tool.creator.get_neetcode_solution")
    @patch("leetcode_study_tool.creator.get_slug")
    def test_generate_problem_with_code(self, mock_get_slug, mock_get_neetcode_solution, mock_get_data):
        mock_get_slug.return_value = "two-sum"
        mock_get_data.return_value = {
            "id": "1",
            "title": "Two Sum",
            "content": "test content",
            "difficulty": "Easy",
            "tags": [],
            "companies": [],
            "solutions": []
        }
        mock_get_neetcode_solution.return_value = "def two_sum(nums, target):\n    # Solution code"
        
        mock_format_anki = MagicMock()
        with patch.dict(
            "leetcode_study_tool.formatters.FORMAT_MAP",
            {"anki": mock_format_anki},
        ):
            mock_problem_creator = creator.ProblemsCreator(self.fake_parsed_args_with_code)
            mock_problem_creator._generate_problem("two-sum")
            
            mock_get_neetcode_solution.assert_called_once_with("1", "Two Sum", "python")
            
            called_args = mock_format_anki.call_args[0]
            self.assertIsNotNone(called_args[2].get("neetcode_solution"))
