#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
import subprocess

from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QFrame, QLabel, QListView, QListWidget)

from epookman.ui.widgets.ebook import (EBOOKFRAME_THUMBNAIL_HEIGHT,
                                       EBOOKFRAME_THUMBNAIL_WIDTH,
                                       EBOOKFRAME_WIDTH, EbookWidget)

ITEMS_SPACING = 15


class ListWidget(QListWidget):

    def __init__(self, QParent, ebookList, parent=None):
        super().__init__(QParent)
        self.parent = parent

        self.setAutoFillBackground(True)
        self.setViewMode(QListView.IconMode)
        self.widgets = {}
        self.set(ebookList)
        self.setResizeMode(QListWidget.Adjust)
        self.setIconSize(
            QSize(EBOOKFRAME_THUMBNAIL_WIDTH, EBOOKFRAME_THUMBNAIL_HEIGHT))
        self.setSpacing(ITEMS_SPACING)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.itemClicked.connect(self.openEbook)

        with open("epookman/ui/QSS/listWidget.qss", "r") as f:
            self.setStyleSheet(f.read())

    def set(self, ebookList):
        self.widgets = dict()
        self.list = ebookList
        for ebook in self.list:
            w = EbookWidget(self, ebook)
            self.addItem(w)
            self.widgets[ebook.name] = w

    def delete(self):
        self.clear()

    def update(self, ebookList):
        self.delete()
        self.set(ebookList)

    def search(self, text):
        items = self.findItems(text, Qt.MatchContains)
        for item in self.widgets.values():
            if item not in items:
                item.setHidden(True)
            else:
                item.setHidden(False)

    def openEbook(self, item):

        ereader = "zathura"
        file = open("/dev/null", "w")
        subprocess.Popen([ereader, item.ebook.get_path()], stderr=file)
        print(item.ebook.get_path())
        file.close()
