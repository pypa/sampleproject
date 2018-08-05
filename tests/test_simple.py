"""
Testing is located here
"""

import logging
import unittest

import sample


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_main(self):
        sample.main()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
