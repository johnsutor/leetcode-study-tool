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
        )
        self.fake_parsed_args_url = argparse.Namespace(
            file=None,
            url="fake-url-one,fake-url-two,fake-url-three",
            output="fake-output",
            format="anki",
            language=None,
        )

    @patch("builtins.open")
    def test_sanitize(self, mock_open):
        mock_problem_creator = creator.ProblemsCreator(
            self.fake_parsed_args_file
        )
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
            mock_problem_creator = creator.ProblemsCreator(
                self.fake_parsed_args_file
            )
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
            mock_problem_creator = creator.ProblemsCreator(
                self.fake_parsed_args_file
            )
            mock_problem_creator._generate_problem("two-sum")
            mock_format_anki.assert_called_once()
