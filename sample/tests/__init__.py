# coding: utf-8
"""Helpers for unit tests."""
from unittest import TestCase


#pylint: disable=R0904
# TestCase23: Too many public methods (48/20)
class TestCase23(TestCase):
    """
    This class let you use the new unittest API (>=3.2),
    even if you're running 2.7
    """

    # Monkey-patch for Python 2/3 compatibility inspired from
    # http://people.canonical.com/~cjwatson/\
    # bzr/cdimage/mainline/lib/cdimage/tests/helpers.py
    if not hasattr(TestCase, 'assertCountEqual'):
        #pylint: disable=E1101
        # E1101=Class 'TestCase' has no 'assertItemsEqual' member
        assertCountEqual = TestCase.assertItemsEqual
    if not hasattr(TestCase, 'assertRegex'):
        assertRegex = TestCase.assertRegexpMatches
    if not hasattr(TestCase, 'assertRaisesRegex'):
        assertRaisesRegex = TestCase.assertRaisesRegexp
