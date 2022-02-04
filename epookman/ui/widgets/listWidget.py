#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QFrame, QLabel, QListView, QListWidget,
                             QListWidgetItem)

from epookman.ui.widgets.ebook import EbookFrame, EbookListWidgetItem

ITEMS_SPACING = 25


class ListWidget(QListWidget):

    def __init__(self, QParent, ebookList, parent=None):
        super().__init__(QParent)
        self.parent = parent

        self.setAutoFillBackground(True)
        self.setViewMode(QListView.IconMode)
        self.items = {}
        self.set(ebookList)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(ITEMS_SPACING)

        with open("epookman/ui/QSS/listWidget.qss", "r") as f:
            self.setStyleSheet(f.read())

    def set(self, ebookList):
        self.widgets = dict()
        self.list = ebookList
        for ebook in self.list:
            w = EbookFrame(self, ebook)
            i = EbookListWidgetItem(self, ebook)
            self.addItem(i)
            self.setItemWidget(i, w)
            self.items[ebook.name] = i

    def delete(self):
        self.items = {}
        self.clear()

    def update(self, ebookList):
        self.delete()
        self.set(ebookList)

    def search(self, text):
        for title in self.items.keys():
            item = self.items[title]
            if text.lower() in title.lower():
                item.show()
            else:
                item.hide()
