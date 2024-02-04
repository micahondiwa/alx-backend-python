#!/usr/bin/env python3
"""
test for utils module
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Dict, Union, Tuple
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    tests for the access_nested_map method
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict, path: Tuple[str], expected: Union[Dict, int]
    ) -> None:
        """tests access_nested_map's output"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",), KeyError), ({"a": 1}, ("a", "b"), KeyError)])
    def test_access_nested_map_exception(
        self, nested_map: Dict, path: Tuple[str], exception: Exception
    ) -> None:
        """tests KeyError exception raised"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json method"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """tests get_json output"""
        attrs = {"json.return_value": test_payload}
        with patch("requests.get", return_value=Mock(**attrs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for decorator memoize"""

    def test_memoize(self) -> None:
        """Tests memoize's output"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=lambda: 42
        ) as memoized_fn:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memoized_fn.assert_called_once()
