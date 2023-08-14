import unittest
from textwrap import dedent

import leetcode_study_tool.formatters as formatters
from leetcode_study_tool.queries import get_data, get_url


class TestFormatters(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.correct_anki_formatted_two_sum_problem = '    <h1>        <a href="https://leetcode.com/problems/two-sum/">1. Two Sum</a>    </h1>    <p>        <p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p><p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p><p>You can return the answer in any order.</p><p>&nbsp;</p><p><strong class="example">Example 1:</strong></p><pre><strong>Input:</strong> nums = [2,7,11,15], target = 9<strong>Output:</strong> [0,1]<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].</pre><p><strong class="example">Example 2:</strong></p><pre><strong>Input:</strong> nums = [3,2,4], target = 6<strong>Output:</strong> [1,2]</pre><p><strong class="example">Example 3:</strong></p><pre><strong>Input:</strong> nums = [3,3], target = 6<strong>Output:</strong> [0,1]</pre><p>&nbsp;</p><p><strong>Constraints:</strong></p><ul>\t<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>\t<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>\t<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>\t<li><strong>Only one valid answer exists.</strong></li></ul><p>&nbsp;</p><strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face="monospace">&nbsp;</font>time complexity?    <p>    <strong>Tags:</strong><br>    <ul>        <li>Array</li><li>Hash Table</li>    </ul>    ;<strong>NeetCode Solution:</strong><br><a href="https://youtube.com/watch?v=KLlXCFG5TnA">Two Sum - Leetcode 1 - HashMap - Python</a></li><br><br>    <strong>LeetCode User Solutions:</strong><br>    <ul>        <li>https://leetcode.com/problems/two-sum/solutions/2/1/</li><li>https://leetcode.com/problems/two-sum/solutions/3/1/</li><li>https://leetcode.com/problems/two-sum/solutions/4/1/</li><li>https://leetcode.com/problems/two-sum/solutions/6/1/</li><li>https://leetcode.com/problems/two-sum/solutions/7/1/</li><li>https://leetcode.com/problems/two-sum/solutions/8/1/</li><li>https://leetcode.com/problems/two-sum/solutions/9/1/</li><li>https://leetcode.com/problems/two-sum/solutions/10/1/</li><li>https://leetcode.com/problems/two-sum/solutions/11/1/</li><li>https://leetcode.com/problems/two-sum/solutions/12/1/</li>    </ul>    ;array hash-table'

    def test_format_list_element(self):
        self.assertEqual(
            dedent(
                formatters.format_list_element(
                    "fake-title", ["fake-el-1", "fake-el-2"]
                )
            ),
            dedent(
                """
            <strong>fake-title:</strong><br>
            <ul>
                <li>fake-el-1</li><li>fake-el-2</li>
            </ul>
            """
            ),
        )

    def test_format_solution_link(self):
        self.assertEqual(
            formatters.format_solution_link("fake-slug", "fake-solution-id"),
            "https://leetcode.com/problems/fake-slug/solutions/fake-solution-id/1/",
        )

    def test_format_anki(self):
        data = get_data("two-sum")
        self.assertEqual(
            formatters.format_anki(get_url("two-sum"), "two-sum", data),
            self.correct_anki_formatted_two_sum_problem,
        )
