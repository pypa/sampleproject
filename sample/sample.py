# coding: utf-8
from sys import argv
from platform import uname


class Sample(object):

    def __init__(self, name=""):
        self.name = name if name else "W°®lð"

    def hello(self):
        template = """Hello {greets} !
I'm {computer}.
Nice to serve U."""
        return template.format(greets=self.name, computer=" ".join(uname()))

if __name__ == "__main__":
    sample = Sample(" ".join(argv[1:]))
    print(sample.hello())
