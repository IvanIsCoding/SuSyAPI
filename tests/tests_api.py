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
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, filename)
    try:
        html_file = open(file_path, "r")
        html_source = html_file.read()
        html_file.close()
        return html_source
    except FileNotFoundError:
        return ""  # the file does not exist, return empty code


# Source of some SuSy pages
HTML_PAGES = {
    "SECTIONS": "examples/maintenance.html",
    "ASSIGNMENT1": "examples/maintenance.html",
    "EMPTY_ASSIGNMENT": "examples/maintenance.html",
    "TASK1": "examples/maintenance.html",
    "TASK2": "examples/maintenance.html",
    "GROUP": "examples/maintenance.html",
    "EMPTY_GROUP": "examples/maintenance.html",
    "MAINTENANCE": "examples/maintenance.html",
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
        mocked_get.return_value = load_example_html(HTML_PAGES["MAINTENANCE"])
        self.assertEqual(susyapi.get_sections(), {})

    def test_get_groups(self):
        pass
        # html_source = load_example_html(HTML_PAGES["TASK1"])
        # url = ""
        # self.assertEqual(susyapi._get_groups(html_source, url), )

    def test_get_due_date(self):
        pass
        # html_source = load_example_html(HTML_PAGES["TASK1"])
        # self.assertEqual(susyapi._get_due_date(html_source), )

        # html_source = load_example_html(HTML_PAGES["TASK2"])
        # self.assertEqual(susyapi._get_due_date(html_source), )

    @patch("susyapi._get_html")
    def test_get_assignments(self, mocked_get):
        mocked_get.return_value = load_example_html(HTML_PAGES["MAINTENANCE"])
        self.assertEqual(susyapi.get_sections(), {})

    @patch("susyapi._get_html")
    def test_get_users(self, mocked_get):

        mock_url = "https://susy.ic.unicamp.br:9999/mc999/01/relatoA.html"

        mocked_get.return_value = load_example_html(HTML_PAGES["MAINTENANCE"])
        self.assertEqual(susyapi.get_users(mock_url), [])

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
