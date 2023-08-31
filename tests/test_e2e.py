import os
import unittest


class TestE2E(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_call(self):
        exit_status = os.system("leetcode-study-tool --help")
        assert exit_status == 0
