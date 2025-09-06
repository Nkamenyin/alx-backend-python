import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    TestCase for the access_nested_map function.

    Tests both successful access and exception raising for invalid keys.
    """

    @parameterized.expand([   # Test cases: (nested_map, path, expected_result)
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
        # Assert the function returns the expected value for the given path
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([ #Test cases where a KeyError should be raised with the missing key
        ({}, ("a",), "a"),            # empty dict, key 'a' missing
        ({"a": 1}, ("a", "b"), "b"), # key 'b' missing in nested map
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
        with self.assertRaises(KeyError) as cm:  # checks for KeyError
            access_nested_map(nested_map, path)
        # Check that the exception message matches the missing key (with quotes)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


# Run tests when script is executed
if __name__ == "__main__":
    unittest.main()