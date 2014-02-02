# coding: utf-8
""" Test for class Sample."""

import unittest
from sample.sample import Sample
from sample.tests import TestCase23


#pylint: disable=R0904
# TestSample: Too many public methods (49/20)
class TestSample(TestCase23):
    """Tests for class Sample."""

    def test_hello(self):
        """Test Sample.hello."""
        regex = r'Hello {name} !\nI\'m .*\nNice to serve U\.'
        test_cases = [(None, "W°®lð"), ("Pythonista", "Pythonista")]

        for arg, result in test_cases:
            self.assertRegex(Sample(arg).hello(), regex.format(name=result))

if __name__ == '__main__':
    unittest.main()
