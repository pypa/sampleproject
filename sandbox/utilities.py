"""
General utilities

"""


import os


def update_path(path_file, lim_depth=5, absolute=True):
    """ bubble in the folder tree up until it found desired file
    otherwise return original one

    :param str path_file: path to the file/folder
    :param int lim_depth: length of bubble attempted
    :param bool absolute: absolute path
    :return str:

    >>> os.path.exists(update_path('tests', absolute=False))
    True
    >>> os.path.exists(update_path('~'))
    True
    >>> os.path.exists(update_path('/'))
    True
    """
    if path_file.startswith('/'):
        return path_file
    elif path_file.startswith('~'):
        path_file = os.path.expanduser(path_file)
    else:
        for _ in range(lim_depth):
            if os.path.exists(path_file):
                break
            path_file = os.path.join('..', path_file)
    if absolute:
        path_file = os.path.abspath(path_file)
    return path_file
