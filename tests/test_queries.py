import unittest
from unittest.mock import call, patch

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
        self.assertRaises(
            ValueError, queries.get_url, self.bad_input, "bad-type"
        )

    @patch("requests.Session.get")
    def test_query(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.fake_api_response
        for content in queries.MAPPINGS.keys():
            self.assertEqual(
                queries.query(content, "fake-slug"), {"fake-key": "fake-value"}
            )

    @patch("requests.get")
    def test_query_raises(self, mock_get):
        self.assertRaises(
            AssertionError,
            queries.query,
            "fake-content",
            "fake-slug",
            fake_kwarg="fake-value",
        )
        mock_get.return_value.status_code = 500
        # self.assertRaises(requests.exceptions.HTTPError, queries.query, "content", "fake-slug")

    @patch("leetcode_study_tool.queries.query")
    def test_get_data(self, mock_query):
        session = queries.generate_session()
        queries.get_data(self.fake_slug, self.fake_language, session)
        calls = [
            call("title", self.fake_slug, session),
            call("content", self.fake_slug, session),
            call("tags", self.fake_slug, session),
            call("companies", self.fake_slug, session),
            call(
                "solutions",
                self.fake_slug,
                session,
                skip=0,
                first=10,
                languageTags=(self.fake_language),
            ),
        ]
        mock_query.assert_has_calls(calls, any_order=True)


if __name__ == "__main__":
    unittest.main()
