"""
Testing is located here
"""

import logging
import unittest

import sandbox


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_main(self):
        sandbox.main()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
