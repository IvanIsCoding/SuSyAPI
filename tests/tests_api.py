import unittest
from unittest.mock import patch, Mock
import requests
import datetime
import os

try:
    import susyapi
except ModuleNotFoundError:
    import sys

    sys.path.append("..")
    import susyapi


def load_example_html(filename):
    """Loads the data from the HTML examples in the examples folder."""
    return ""


# Source of some SuSy pages
HTML_PAGES = {
    "SECTIONS": "",
    "ASSIGNMENT1": "",
    "EMPTY_ASSIGNMENT": "",
    "TASK1": "",
    "TASK2": "",
    "GROUP": "",
    "EMPTY_GROUP": "",
}


class TestArguments(unittest.TestCase):
    def test_format_user_id(self):
        self.assertEqual(susyapi._format_user_id("ra123456"), "123456")
        self.assertEqual(susyapi._format_user_id("123456"), "123456")
        self.assertEqual(susyapi._format_user_id("1"), "1")
        self.assertEqual(susyapi._format_user_id("ra1"), "1")
        self.assertEqual(susyapi._format_user_id("ra"), "ra")

    @patch("requests.get")
    def test_get_html(self, mocked_get):
        """This test mocks requests.get to avoid having to access external data.
        A Mock object is used to replace the answer to the query and return
        the HTML of the main page.
        """

        mocked_response = Mock()
        mocked_response.text = HTML_PAGES["SECTIONS"]

        mocked_get.return_value = mocked_response
        self.assertEqual(susyapi._get_html("url"), HTML_PAGES["SECTIONS"])

    @patch("susyapi._get_html")
    def test_get_sections(self, mocked_get):
        pass

    def test_get_groups(self):
        html_source = load_example_html(HTML_PAGES["TASK1"])
        url = ""
        # self.assertEqual(susyapi._get_groups(html_source, url), )

    def test_get_due_date(self):

        html_source = load_example_html(HTML_PAGES["TASK1"])
        # self.assertEqual(susyapi._get_due_date(html_source), )

        html_source = load_example_html(HTML_PAGES["TASK2"])
        # self.assertEqual(susyapi._get_due_date(html_source), )

    @patch("susyapi._get_html")
    def test_get_assignments(self, mocked_get):
        pass

    @patch("susyapi._get_html")
    def test_get_users(self, mocked_get):

        mock_url = "url"

        mocked_get.return_value = load_example_html(HTML_PAGES["GROUP"])
        # self.assertEqual(susyapi.get_users(), ["visita"])

        mocked_get.return_value = load_example_html(HTML_PAGES["EMPTY_GROUP"])
        self.assertEqual(susyapi.get_users(mock_url), [])

    def test_type_error(self):
        self.assertRaises(TypeError, susyapi._format_user_id, [])
        self.assertRaises(TypeError, susyapi._get_html, 0)
        self.assertRaises(TypeError, susyapi._get_html, "", 0)
        self.assertRaises(TypeError, susyapi.get_sections, {})
        self.assertRaises(TypeError, susyapi.get_assignments, {})
        self.assertRaises(TypeError, susyapi.get_users, {})
        self.assertRaises(TypeError, susyapi._get_groups, "", [])
        self.assertRaises(TypeError, susyapi._get_groups, [], "")
        self.assertRaises(TypeError, susyapi._get_due_date, [])


if __name__ == "__main__":
    unittest.main()
