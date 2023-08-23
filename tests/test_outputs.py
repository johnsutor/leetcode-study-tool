import unittest
from unittest.mock import patch

import leetcode_study_tool.outputs as outputs


class TestSavers(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch("builtins.open")
    def test_save_string(self, mock_open):
        outputs.save_string(["fake-string"], "fake-file")
        mock_open.assert_called_once_with("fake-file.txt", "w")

    @patch("xlsxwriter.Workbook")
    def test_save_excep(self, mock_workbook):
        fake_formatted_output = [
            "fake_id",
            "fake_title",
            "fake_url",
            "fake_date attempted",
            "fake_tags",
            "fake_neetcode",
            "fake_solutions",
            "fake_companies",
        ]

        outputs.save_excel(fake_formatted_output, "fake-file")
        mock_workbook.assert_called_once_with("fake-file.xlsx")
