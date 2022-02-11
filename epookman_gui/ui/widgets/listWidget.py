#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

# TODO: Maybe change to QListView
import subprocess

from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QAction, QFrame, QListView, QListWidget,
                             QListWidgetItem, QMenu)
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
        self.installEventFilter(self)
        self.itemDoubleClicked.connect(self.openEbook)

        self.setContextMenu()

    def setContextMenu(self):
        self.menu = QMenu()

        self.menu.setObjectName("contextMenu")
        self.open = QAction("Open")
        self.addFav = QAction("Add to Fav")
        self.markAsToRead = QAction("Mark as To Read")
        self.markAsDone = QAction("Mark as Done")
        self.delFav = QAction("Remove from Fav")

        self.menu.addAction(self.open)
        self.menu.addAction(self.addFav)
        self.menu.addAction(self.markAsToRead)
        self.menu.addAction(self.markAsDone)
        self.menu.addAction(self.delFav)

        self.menu.setCursor(QCursor(Qt.PointingHandCursor))

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self:

            menu_click = self.menu.exec_(event.globalPos())
            item = source.itemAt(event.pos())

            if not item:
                return False

            if menu_click == self.open:
                self.openEbook(item)

            if menu_click == self.addFav:
                item.markFav(True)

            elif menu_click == self.delFav:
                item.markFav(False)

            elif menu_click == self.markAsDone:
                item.markDone()

            elif menu_click == self.markAsToRead:
                item.markToRead()

        return super(ListWidget, self).eventFilter(source, event)

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

    def openEbook(self, item):
        ereader = "zathura"
        errFile = open("/dev/null", "w")
        subprocess.Popen([ereader, item.ebook.path], stderr=errFile)
        item.markReading()
