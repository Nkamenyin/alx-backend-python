#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
    """
    TestCase for the access_nested_map function.

    Tests both successful access and exception raising for invalid keys.
    """

    @parameterized.expand([
        # Test cases: (nested_map, path, expected_result)
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected result for valid inputs.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): Tuple of keys representing the path to the value.
            expected: The expected value returned by access_nested_map.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # Test cases where a KeyError should be raised with the missing key
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Test that access_nested_map raises KeyError with the correct message
        when a key in the path does not exist.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): Tuple of keys representing the path to the value.
            expected_key (str): The key expected to be missing and raised in KeyError.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    TestCase for the utils.get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected payload by mocking requests.get.

        Args:
            test_url (str): The URL to fetch.
            test_payload (dict): The expected JSON payload to be returned.
            mock_get (Mock): The mocked requests.get function.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()