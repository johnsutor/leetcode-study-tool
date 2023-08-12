import argparse
import unittest
from unittest.mock import patch

import leetcode_study_tool.cli as cli


class TestCli(unittest.TestCase):
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
            format=None,
            language=None,
        )
        self.fake_parsed_args_url = argparse.Namespace(
            file=None,
            url="fake-url-one,fake-url-two,fake-url-three",
            output="fake-output",
            format=None,
            language=None,
        )

        self.correct_two_sum_problem = (
            b'<h1><a href="https://leetcode.com/problems/two-sum/">1. Two'
            b" Sum</a></h1><p>Given an array of integers"
            b" <code>nums</code>\xc2\xa0and an integer <code>target</code>,"
            b" return <em>indices of the two numbers such that they add up to"
            b" <code>target</code></em>.</p>  <p>You may assume that each input"
            b" would have <strong><em>exactly</em> one solution</strong><br>,"
            b" and you may not use the <em>same</em> element twice.</p>  <p>You"
            b" can return the answer in any order.</p>  <p>\xc2\xa0</p>"
            b' <p><strong class="example">Example 1:</strong><br></p>  <pre>'
            b" <strong>Input:</strong><br> nums = [2,7,11,15], target = 9"
            b" <strong>Output:</strong><br> [0,1]"
            b" <strong>Explanation:</strong><br> Because nums[0] + nums[1] =="
            b' 9, we return [0, 1]. </pre>  <p><strong class="example">Example'
            b" 2:</strong><br></p>  <pre> <strong>Input:</strong><br> nums ="
            b" [3,2,4], target = 6 <strong>Output:</strong><br> [1,2] </pre> "
            b' <p><strong class="example">Example 3:</strong><br></p>  <pre>'
            b" <strong>Input:</strong><br> nums = [3,3], target = 6"
            b" <strong>Output:</strong><br> [0,1] </pre>  <p>\xc2\xa0</p>"
            b" <p><strong>Constraints:</strong><br></p>  <ul> \t<li><code>2 <="
            b" nums.length <= 10<sup>4</sup></code></li>"
            b" \t<li><code>-10<sup>9</sup> <= nums[i] <="
            b" 10<sup>9</sup></code></li> \t<li><code>-10<sup>9</sup> <= target"
            b" <= 10<sup>9</sup></code></li> \t<li><strong>Only one valid"
            b" answer exists.</strong><br></li> </ul>  <p>\xc2\xa0</p>"
            b" <strong>Follow-up:\xc2\xa0</strong><br>Can you come up with an"
            b" algorithm that is less than <code>O(n<sup>2</sup>)</code><font"
            b' face="monospace">\xc2\xa0</font>time'
            b" complexity?<br><ul><strong>Tags:</strong><br><li>Array</li><li>Hash"
            b" Table</li></ul>;<ul><strong>NeetCode Solution:</strong><br><a"
            b' href="https://youtube.com/watch?v=KLlXCFG5TnA">Two Sum -'
            b" Leetcode 1 - HashMap - Python</a></li><br><br><strong>LeetCode"
            b" User Solutions:</strong><br><li><a"
            b' href="https://leetcode.com/problems/two-sum/solutions/2/1/">https://leetcode.com/problems/two-sum/solutions/2/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/3/1/">https://leetcode.com/problems/two-sum/solutions/3/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/4/1/">https://leetcode.com/problems/two-sum/solutions/4/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/6/1/">https://leetcode.com/problems/two-sum/solutions/6/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/7/1/">https://leetcode.com/problems/two-sum/solutions/7/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/8/1/">https://leetcode.com/problems/two-sum/solutions/8/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/9/1/">https://leetcode.com/problems/two-sum/solutions/9/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/10/1/">https://leetcode.com/problems/two-sum/solutions/10/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/11/1/">https://leetcode.com/problems/two-sum/solutions/11/1/</a></li><li><a'
            b' href="https://leetcode.com/problems/two-sum/solutions/12/1/">https://leetcode.com/problems/two-sum/solutions/12/1/</a></li></ul>;array'
            b" hash-table"
        )

    def test_sanitize(self):
        self.assertEqual(
            cli.sanitize(self.fake_string_to_sanitize),
            "<strong>fake<string\xa0to>sanitize</strong><br> <p> More  content"
            " to sanitize </p><br>",
        )

    def test_generate_solution_link(self):
        self.assertEqual(
            cli.generate_solution_link("fake-slug", "fake-solution-id"),
            "https://leetcode.com/problems/fake-slug/solutions/fake-solution-id/1/",
        )

    @patch("builtins.open")
    def test_save_output(self, mock_open):
        cli.save_output(["fake-problem"], "fake-file")
        mock_open.assert_called_with("fake-file", "w")

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_args(self, mock_parse_args):
        mock_parse_args.return_value = "fake-args"
        self.assertEqual(cli.parse_args(), "fake-args")

    def test_generate_problem(self):
        result = cli.generate_problem("https://leetcode.com/problems/two-sum/")
        result = result.encode("utf-8")
        self.assertEqual(result, self.correct_two_sum_problem)

    @patch("leetcode_study_tool.cli.save_output")
    @patch("multiprocessing.pool.Pool")
    @patch("builtins.open")
    def test_cli_file(self, mock_open, mock_pool, mock_save_output):
        cli.cli(self.fake_parsed_args_file)
        mock_open.assert_called_with("fake-file", "r")
        mock_pool.assert_called_once()

    @patch("leetcode_study_tool.cli.save_output")
    @patch("multiprocessing.pool.Pool")
    @patch("builtins.open")
    def test_cli_url(self, mock_open, mock_pool, mock_save_output):
        cli.cli(self.fake_parsed_args_url)
        mock_pool.assert_called_once()


if __name__ == "__main__":
    unittest.main()
