import unittest
from unittest.mock import patch

import leetcode_study_tool.cli as cli


class TestCli(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch("argparse.ArgumentParser.parse_args")
    def test_generate_args(self, mock_parse_args):
        mock_parse_args.return_value = "fake-args"
        self.assertEqual(cli.generate_parser().parse_args(), "fake-args")
