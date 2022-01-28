#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""File system scraper"""

import os
from sys import stderr


def check_path(path):
    if not os.path.lexists(path):
        return False

    return True

class Dirent():

    def __init__(self, uri=""):

        self.path = uri
        self.files = list()
        self.recurs = 1

    def toggle_recurs(self):
        self.recurs = not self.recurs

    def getfiles_from_path(self, path):
        if not check_path(path):
            return

        ents = os.scandir(path)

        for ent in ents:
            if os.path.isdir(ent.path):
                if self.recurs:
                    self.getfiles_from_path(ent.path)
                else:
                    continue

            else:
                self.files.append(ent.path)

    def getfiles(self):
        path = self.path
        self.getfiles_from_path(path)

    def set_values(self, uri, recurs):
        self.path = uri
        self.recurs = recurs

    def __str__(self):
        return self.path
