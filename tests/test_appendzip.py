# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
import pathlib
from os import remove
from zipfile import ZipFile

from src.appendzip.appendzip import appendzip

test_zip_path = pathlib.Path("test.zip")
delta = 33


def createZip():
    with ZipFile('test.zip', 'w') as testzip:
        testzip.write('LICENSE.txt', 'LICENSE.txt')

    with ZipFile('test.zip', 'r') as testzip:
        fromzip = testzip.read('LICENSE.txt')
    return fromzip


def deleteZip():
    if test_zip_path.exists():
        remove(test_zip_path)


class TestAppendZip(unittest.TestCase):

    def test_create_zip(self):
        fromzip = createZip()
        license = open('LICENSE.txt').read()
        self.assertAlmostEqual(len(fromzip), len(license), delta=delta)
        deleteZip()

    def test_append_zip(self):
        createZip()
        appendzip(
            pathlib.Path('test.zip'),
            pathlib.Path('README.md'),
            'LICENSE.txt'
        )

        with ZipFile('test.zip', 'r') as testzip:
            infolist = testzip.infolist()
            self.assertEqual(
                len(infolist),
                1,
                "wrong number of files in zip {}"
                .format(infolist)
            )
            fromzip = testzip.read('LICENSE.txt')

        readme = open('README.md').read()
        self.assertAlmostEqual(len(fromzip), len(readme), delta=delta)
        deleteZip()

    def test_delete_zip(self):
        createZip()
        deleteZip()
        self.assertFalse(test_zip_path.exists())


if __name__ == '__main__':
    unittest.main()
