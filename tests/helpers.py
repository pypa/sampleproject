# coding: utf-8

from pylint.lint import Run as run_pylint
from pep8 import _main as run_pep8

def run_check_lint():
    """Run pylint with proper config file."""
    run_pylint(['--rcfile=.pylintrc', 'sample'])

def run_check_pep8():
    """Run pep8 by hacking argv."""
    from sys import argv
    argv += ['sample']
    run_pep8()
