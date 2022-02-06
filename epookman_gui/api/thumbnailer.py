#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""PDF thumbnailer"""

from os import path
import subprocess


def thumbnailer(file, output):
    if ".pdf" not in file:
        return -1
    if path.lexists(file):
        errFile = open("/dev/null", "w")
        return subprocess.run(
            ["pdftocairo", "-singlefile", file, "-png", output],
            stderr=errFile)
    else:
        print("File %s does not exists" % file)
