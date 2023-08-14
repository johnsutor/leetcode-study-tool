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
