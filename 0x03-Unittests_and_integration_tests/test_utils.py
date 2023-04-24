#!/usr/bin/env python3
"""Test module for the `utils` module.

This module tests the following functions from the `utils` module:
    - `access_nested_map`
    - `get_json`
    - `memoize`
"""

import unittest
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the `access_nested_map` function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map_returns_expected_value(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: Union[Dict, int]
    ) -> None:
        """Test that `access_nested_map` returns the expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_raises_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            exception: Exception
    ) -> None:
        """Test that `access_nested_map` raises the expected exception."""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test case for the `get_json` function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json_returns_expected_value(
            self,
            test_url: str,
            test_payload: Dict,
    ) -> None:
        """Test that `get_json` returns the expected value."""
        attrs = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**attrs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test case for the `memoize` function."""

    def test_memoize_returns_expected_value(self) -> None:
        """Test that `memoize` returns the expected value."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=lambda: 42) as memo_fxn:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_fxn.assert_called_once()
