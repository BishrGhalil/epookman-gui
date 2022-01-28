#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""The Main Class responsible to initialize the EM object and stuff."""

import curses
import pdb
from sys import argv

from PyQt5 import QtCore, QtGui, QtWidgets
from epookman.ui.widgets.mainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()


def main():
    if len(argv) > 1:
        if "-h" in argv or "--help" in argv:
            print("Usage: epookman [OPTIONS]\n")
            print("There no options.")
            exit(0)
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    return app.exec_()
