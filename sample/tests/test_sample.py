# coding: utf-8
import unittest
from sample.sample import Sample
from sample.tests import TestCase23


class TestSample(TestCase23):

    def test_hello(self):
        regex = r'Hello {name} !\nI\'m .*\nNice to serve U\.'
        test_cases = [(None, "W°®lð"), ("Pythonista", "Pythonista")]

        for arg, result in test_cases:
            self.assertRegex(Sample(arg).hello(), regex.format(name=result))

if __name__ == '__main__':
    unittest.main()
