#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""The Main Class responsible to initialize the EM object and stuff."""

import curses
import pdb
from sys import argv
from os import (getenv, path, mkdir)

from PyQt5 import (QtCore, QtGui, QtWidgets)
from epookman.ui.widgets.mainWindow import (Ui_MainWindow)
from epookman.api.db import *
from epookman.api.search import scane_commit


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()


def createDirs():
    home = getenv("HOME")

    cache = path.join(home, ".cache", "epookman-gui")
    if not path.lexists(cache):
        mkdir(cache)
    thumbnails = path.join(home, ".cache", "epookman-gui", "thumbnails")
    if not path.lexists(thumbnails):
        mkdir(thumbnails)

    config = path.join(home, ".config", "epookman-gui")
    if not path.lexists(config):
        mkdir(config)


def main():
    if len(argv) > 1:
        if "-h" in argv or "--help" in argv:
            print("Usage: epookman [OPTIONS]\n")
            print("There no options.")
            exit(0)

    createDirs()
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    return app.exec_()
