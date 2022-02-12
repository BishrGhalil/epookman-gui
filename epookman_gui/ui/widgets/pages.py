#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtWidgets import (QFrame, QStackedWidget, QVBoxLayout)

from epookman_gui.ui.widgets.ebookPage import EbookPage
from epookman_gui.ui.widgets.settingsPage import SettingsPage


class Pages(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("pages")
        self.parent = parent
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("pages_layout")
        self.layout.setSpacing(0)

        self.setStack()
        self.setPages()

        self.layout.addWidget(self.stack)

    def setEbookPages(self):
        self.readingPage = EbookPage("READING")
        self.toreadPage = EbookPage("TO READ")
        self.donePage = EbookPage("DONE")
        self.allPage = EbookPage("ALL")
        self.favPage = EbookPage("FAV")

        self.pages["READING"] = self.readingPage
        self.pages["TO READ"] = self.toreadPage
        self.pages["DONE"] = self.donePage
        self.pages["ALL"] = self.allPage
        self.pages["FAV"] = self.favPage

    def setSettingsPage(self):
        settingsPage = SettingsPage(self)
        self.settingsPage = settingsPage
        self.pages["SETTINGS"] = self.settingsPage

    def setPages(self):
        self.pages = {}

        self.setEbookPages()
        self.setSettingsPage()

        for page in self.pages.values():
            self.stack.addWidget(page)

    def setStack(self):
        self.stack = QStackedWidget(self)
        self.stack.setObjectName("pages_stack")

    def changePage(self, name):
        page = self.pages[name]
        pagesList = [page for page in self.pages.values()]
        index = pagesList.index(page)
        self.stack.setCurrentIndex(index)
        page.update()
