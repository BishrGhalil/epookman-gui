# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENSE" for details.
"""A terminal ebook manager written in Python. Inspired by ranger file manager. It supports VI key bindings, And provides a minimalistic curses interface.
"""

import os
from sys import version_info


# Version helper
def version_helper():
    if __release__:
        version_string = 'epookman {0}'.format(__version__)
    else:
        import subprocess
        version_string = 'epookman-master {0}'
        try:
            with subprocess.Popen(
                ["git", "describe"],
                    universal_newlines=True,
                    cwd=EPOOKMANDIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
            ) as git_describe:
                (git_description, _) = git_describe.communicate()
            version_string = version_string.format(git_description.strip('\n'))
        except (OSError, subprocess.CalledProcessError, AttributeError):
            version_string = version_string.format(__version__)
    return version_string


# Information
__license__ = 'MIT'
__version__ = '0.0.1'
__release__ = False
__author__ = __maintainer__ = 'Beshr Ghalil'
__email__ = 'beshrghalil@porotonmail.com'

# Constants
EPOOKMANDIR = os.path.dirname(__file__)
DEFAULT_PAGER = 'less'
USAGE = '%prog [options] [path]'
VERSION = version_helper()
PY3 = version_info[0] >= 3

args = None

from epookman.core.main import main
