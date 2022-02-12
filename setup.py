#!/usr/bin/env python
# This file is part of epookman_gui.
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
DESCRIPTION = 'Qt ebook manager'
LONG_DESCRIPTION = "epookman-gui is the gui interface for epookman ebook manager."


class InstallExec(distutils.cmd.Command):
    """A custom command to install epookman-gui to path."""

    description = 'install epookman-gui to path'
    user_options = list()

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Copy epookman-gui to path
        logname = os.getlogin()
        home = os.path.join("/home", logname)
        dest_path = os.path.join(home, '.local/bin/epookman-gui')
        here = os.path.abspath(os.path.dirname(__file__))
        src_path = os.path.join(here, "epookman-gui.py")
        shutil.copy(src_path, dest_path)

        # Copy epookman-gui resources and themes to config directory
        config_path = os.path.join(home, ".config/epookman-gui")
        if not os.path.lexists(config_path):
            os.mkdir(config_path)

        themes_path = os.path.join(here, "epookman_gui/ui/themes")
        themes_dist = os.path.join(config_path, "themes")
        resources_path = os.path.join(here, "epookman_gui/ui/resources")
        resources_dist = os.path.join(config_path, "resources")

        if os.path.lexists(themes_dist):
            shutil.rmtree(themes_dist)
        shutil.copytree(themes_path, themes_dist)

        if os.path.lexists(resources_dist):
            shutil.rmtree(resources_dist)
        shutil.copytree(resources_path, resources_dist)


# Setting up
setup(name="epookman-gui",
      version=VERSION,
      author="Beshr Ghalil",
      author_email="<beshrghalil@protonmail.com>",
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      long_description=long_description,
      packages=find_packages(),
      url='https://github.com/BishrGhalil/epookman-gui',
      install_requires=['file-magic', 'PyQt5', 'PyPDF2', 'epub_meta'],
      keywords=['python', 'ebook', 'qt', 'ebook manager', 'gui'],
      classifiers=[
          'Environment :: Desktop',
          'Development Status :: 1 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT',
          'Programming Language :: Python :: 3',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Utilities',
          'Topic :: Desktop Environment :: Ebook Managers',
      ],
      cmdclass={'install_exec': InstallExec})
