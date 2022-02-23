#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""The Main Class responsible to initialize the EM object and stuff."""

from sys import argv
from os import (getenv, path, mkdir)

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from epookman_gui.ui.widgets.mainWindow import (Ui_MainWindow)
from epookman_gui.api.db import (DB_PATH, connect, create_tables,
                                 commit_option)


class MainWindow(QMainWindow):

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
            print("Usage: epookman-gui [OPTIONS]\n")
            print("There no options.")
            exit(0)

    createDirs()
    conn = connect(DB_PATH)
    create_tables(conn)
    conn.close()
    app = QApplication(argv)
    window = MainWindow()
    return app.exec_()
