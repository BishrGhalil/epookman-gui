#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QFrame, QLabel, QListView, QListWidget,
                             QListWidgetItem)
from timeIt import timeIt

from epookman_gui.ui.widgets.ebook import (THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH,
                                           EbookItem)

ITEMS_SPACING = 25


class ListWidget(QListWidget):

    def __init__(self, QParent, ebookList, parent=None):
        super().__init__(QParent)
        self.parent = parent

        self.setAutoFillBackground(True)
        self.setViewMode(QListView.IconMode)
        self.items = {}
        self.itemsSet = set()
        self.set(ebookList)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(ITEMS_SPACING)
        self.setIconSize(QSize(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))

        with open("epookman_gui/ui/QSS/listWidget.qss", "r") as f:
            self.setStyleSheet(f.read())

    def checkEbookItem(self, ebook):
        if self.items.get(ebook.name):
            return True
        else:
            return False

    def createAddItem(self, ebook):
        item = EbookItem(self, ebook)
        self.addItem(item)
        self.items[ebook.name] = item
        self.itemsSet.add(ebook.name)

    def getItemByName(self, ebookName):
        item = self.items[ebookName]
        return item

    def removeItem(self, item):
        row = self.row(item)
        self.takeItem(row)

    def set(self, ebookList):
        self.items = dict()
        for ebook in ebookList:
            self.createAddItem(ebook)

    def delete(self):
        self.items = {}
        self.clear()

    def update(self, ebookList):
        ebooks = {ebook.name: ebook for ebook in ebookList}
        newEbooksSet = set(ebooks.keys())
        toRemove = self.itemsSet.difference(newEbooksSet)
        toCreate = newEbooksSet.difference(self.itemsSet)
        for ebookName in toRemove:
            item = self.getItemByName(ebookName)
            self.removeItem(item)

        for ebookName in toCreate:
            ebook = ebooks[ebookName]
            self.createAddItem(ebook)

        self.itemsSet = newEbooksSet

    def search(self, text):
        for title in self.items.keys():
            item = self.items[title]
            if text.lower() in title.lower():
                item.show()
            else:
                item.hide()
