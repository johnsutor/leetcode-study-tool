import os
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

import leetcode_study_tool.outputs as outputs
from leetcode_study_tool.formatters import EXCEL_COLUMNS


class TestSavers(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_excel_row = [
            "1",
            "Two Sum",
            "Easy",
            "https://leetcode.com/problems/two-sum/",
            date(2024, 1, 15),
            "Array, Hash Table",
            "https://youtube.com/watch?v=video123",
            "https://youtube.com/watch?v=short123",
            "",
            "https://leetcode.com/problems/two-sum/solutions/12345/1/",
            "Amazon, Google",
        ]

    @patch("builtins.open")
    def test_save_string(self, mock_open):
        outputs.save_string(["fake-string"], "fake-file")
        mock_open.assert_called_once_with("fake-file.txt", "w")

    @patch("xlsxwriter.Workbook")
    def test_save_excel(self, mock_workbook):
        outputs.save_excel([self.fake_excel_row], "fake-file")
        mock_workbook.assert_called_once_with("fake-file.xlsx")

    def test_save_excel_creates_file(self):
        test_file = os.path.join(tempfile.gettempdir(), "test_leetcode_output")
        try:
            outputs.save_excel([self.fake_excel_row], test_file)
            self.assertTrue(os.path.exists(test_file + ".xlsx"))
        finally:
            if os.path.exists(test_file + ".xlsx"):
                os.remove(test_file + ".xlsx")

    def test_save_excel_column_count_matches(self):
        self.assertEqual(
            len(self.fake_excel_row),
            len(EXCEL_COLUMNS),
            "Excel row length must match EXCEL_COLUMNS header count",
        )

    def test_save_excel_skips_none_problems(self):
        test_file = os.path.join(tempfile.gettempdir(), "test_leetcode_none")
        try:
            outputs.save_excel([None, self.fake_excel_row, None], test_file)
            self.assertTrue(os.path.exists(test_file + ".xlsx"))
        finally:
            if os.path.exists(test_file + ".xlsx"):
                os.remove(test_file + ".xlsx")

    @patch("builtins.open")
    def test_save_string_skips_none(self, mock_open):
        mock_file = mock_open.return_value.__enter__.return_value
        outputs.save_string([None, "problem-one", None, "problem-two"], "fake-file")
        self.assertEqual(mock_file.write.call_count, 2)
