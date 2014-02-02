# coding: utf-8
"""Describe your module here."""

from sys import argv
from platform import uname


#pylint: disable=R0903
# Sample: Too few public methods (1/2)
class Sample(object):
    """This class holds a name, and his able to greet."""

    def __init__(self, name=""):
        self.name = name if name else "W°®lð"

    def hello(self):
        """Greets the user and print uname details."""
        template = """Hello {greets} !
I'm {computer}.
Nice to serve U."""
        return template.format(greets=self.name, computer=" ".join(uname()))

def main():
    """Entry point for the application script"""
    SAMPLE = Sample(" ".join(argv[1:]))
    print(SAMPLE.hello())

if __name__ == "__main__":
    main()
