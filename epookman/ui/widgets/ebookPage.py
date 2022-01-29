#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit,
                             QScrollArea, QVBoxLayout, QWidget)

from epookman.api.db import DB_PATH, connect, fetch_ebooks
from epookman.ui.widgets.grid import Grid
from epookman.api.ebook import Ebook

EBOOKPAGE_SEARCH_WIDTH = 300


class EbookPageContent(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("ebookpage_content")
        self.parent = parent
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(30, 0, 30, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("ebookpage_content_layout")

        conn = connect(DB_PATH)
        ebookList = fetch_ebooks(conn)
        conn.close()

        grid = Grid(self, ebookList)
        self.setGrid(grid)

        self.setScrollArea()
        self.setLayoutes()

    def setScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("ebookpage_content_scrollArea")

        self.scrollAreaContent = QWidget()
        self.scrollAreaContent.setGeometry(QRect(0, 0, 830, 453))
        self.scrollAreaContent.setMaximumSize(QSize(16777215, 16777215))
        self.scrollAreaContent.setObjectName("scrollAreaContent")
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaContent)
        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")

    def setLayoutes(self):
        self.scrollAreaLayout.addWidget(self.grid)
        self.scrollArea.setWidget(self.scrollAreaContent)

        self.layout.addWidget(self.scrollArea)

    def setGrid(self, grid):
        self.grid = grid


class EbookPage(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName("pages_ebookpage")
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("ebookpage_layout")
        with open("epookman/ui/QSS/ebookPage.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setTopBar()

        self.setLabels()
        self.setInputs()

        content = EbookPageContent(self)
        self.setContent(content)

        self.setLayoutes()

    def setTopBar(self):
        self.topbar = QFrame(self)
        self.topbar.setMaximumSize(QSize(16777215, 130))
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setObjectName("ebookpage_topbar")
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setContentsMargins(30, 50, 60, 10)
        self.topbarLayout.setSpacing(0)
        self.topbarLayout.setObjectName("ebookPage_topbar_layout")

    def setLabels(self):
        self.pageName = QLabel(self.topbar)
        self.pageName.setObjectName("ebookpage_pagename")
        self.setPageName("EBOOKMAN")

    def setInputs(self):
        self.search = QLineEdit(self.topbar)
        self.search.setMaximumSize(QSize(EBOOKPAGE_SEARCH_WIDTH, 16777215))
        self.search.setObjectName("ebookpage_search")
        self.search.setPlaceholderText("Search")

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.pageName)
        self.topbarLayout.addWidget(self.search)

        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)

    def setContent(self, content):
        self.content = content

    def setPageName(self, name):
        self.pageName.setText(name)

    def connectFetchList(self, where=None):
        conn = connect(DB_PATH)
        ebookList = fetch_ebooks(conn, where=where)
        conn.close()
        return ebookList

    def changeEbookPage(self, name):
        self.setPageName(name)
        if name == "READING":
            self.ebookList = self.connectFetchList(
                where=f"STATUS={Ebook.STATUS_READING}")
        elif name == "TO READ":
            self.ebookList = self.connectFetchList(
                where=f"STATUS={Ebook.STATUS_HAVE_NOT_READ}")
        elif name == "DONE":
            self.ebookList = self.connectFetchList(
                where=f"STATUS={Ebook.STATUS_HAVE_READ}")
        elif name == "ALL":
            self.ebookList = self.connectFetchList()
        elif name == "FAV":
            self.ebookList = self.connectFetchList(where=f"FAV={1}")

        self.content.grid.update(self.ebookList)
