# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
from unittest.mock import patch
from io import StringIO

from sample.simple import add_one
from sample import main


class TestSimple(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(add_one(5), 6)

    def test_main(self):
        """Проверяем, что функция main() печатает нужный текст"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(
                fake_out.getvalue().strip(),
                "Call your main application code here"
            )


if __name__ == '__main__':
    unittest.main()