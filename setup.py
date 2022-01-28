#!/usr/bin/env python
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.import codecs

import codecs
import distutils.cmd
import os
import shutil

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Ranger like ebook manager that supports VI key bindings'
LONG_DESCRIPTION = "epookman is a terminal ebook manager written in Python. Inspired by ranger file manager.\nIt supports VI key bindings, And provides a minimalistic curses interface."


class InstallExec(distutils.cmd.Command):
    """A custom command to install epookman to path."""

    description = 'install epookman to path'
    user_options = list()

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        home = os.getenv("HOME")
        dest_paths = ['/usr/bin/epookman']
        here = os.path.abspath(os.path.dirname(__file__))
        src_path = os.path.join(here, "epookman.py")
        for dest_path in dest_paths:
            shutil.copy(src_path, dest_path)

# Setting up
setup(
    name="epookman",
    version=VERSION,
    author="Beshr Ghalil",
    author_email="<beshrghalil@protonmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/BishrGhalil/epookman',
    install_requires=['file-magic', 'curses-utils', 'PyPDF2', 'epub_meta'],
    keywords=['python', 'ebook', 'vim', 'console', 'ebook manager', 'curses'],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Topic :: Desktop Environment :: Ebook Managers',
    ],
    cmdclass={'install_exec': InstallExec}
)
