# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import contextlib
import io
import unittest

from sample.cli import greet
from sample.simple import add_one


class TestSimple(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(add_one(5), 6)

    def test_greet_defaults_to_world(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            greet([])

        self.assertEqual(output.getvalue(), "Hello, World\n")

    def test_greet_accepts_custom_name(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            greet(["--name", "Alice"])

        self.assertEqual(output.getvalue(), "Hello, Alice\n")


if __name__ == '__main__':
    unittest.main()
