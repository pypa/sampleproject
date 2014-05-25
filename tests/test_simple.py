import unittest

import sample


class TestSimple(unittest.TestCase):
    
    def test_failure(self):
        self.assertTrue(False)
