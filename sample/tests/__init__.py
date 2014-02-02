# coding: utf-8
from unittest import TestCase


class TestCase23(TestCase):

    # Monkey-patch for Python 2/3 compatibility inspired from
    # http://people.canonical.com/~cjwatson/\
    # bzr/cdimage/mainline/lib/cdimage/tests/helpers.py
    if not hasattr(TestCase, 'assertCountEqual'):
        assertCountEqual = TestCase.assertItemsEqual
    if not hasattr(TestCase, 'assertRegex'):
        assertRegex = TestCase.assertRegexpMatches
    if not hasattr(TestCase, 'assertRaisesRegex'):
        assertRaisesRegex = TestCase.assertRaisesRegexp
