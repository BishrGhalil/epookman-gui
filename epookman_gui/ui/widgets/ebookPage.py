#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit,
                             QScrollArea, QVBoxLayout, QWidget)

from epookman_gui.api.db import DB_PATH, connect, fetch_ebooks
from epookman_gui.ui.widgets.listWidget import ListWidget
from epookman_gui.api.ebook import Ebook

EBOOKPAGE_SEARCH_WIDTH = 300


class EbookPageContent(QFrame):

    def __init__(self, QParent, name, parent=None):
        super().__init__(QParent)
        self.setObjectName("ebookpageContent")
        self.parent = parent
        self.name = name

        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(30, 0, 30, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("ebookpageContentLayout")

        self.setEbookList()
        self.setListGrid()
        self.setScrollArea()
        self.setLayoutes()
        self.installEventFilter(self)

    def getEbookList(self, name):
        filterClause = None
        if name == "READING":
            filterClause = f"STATUS={Ebook.STATUS_READING}"
        elif name == "TO READ":
            filterClause = f"STATUS={Ebook.STATUS_HAVE_NOT_READ}"
        elif name == "DONE":
            filterClause = f"STATUS={Ebook.STATUS_HAVE_READ}"
        elif name == "FAV":
            filterClause = f"FAV={1}"

        conn = connect(DB_PATH)
        ebookList = fetch_ebooks(conn, where=filterClause)
        conn.close()
        return ebookList

    def setEbookList(self):
        ebookList = self.getEbookList(self.name)
        self.ebookList = ebookList

    def setScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("ebookpageContentScrollArea")

        self.scrollAreaContent = QWidget()
        self.scrollAreaContent.setGeometry(QRect(0, 0, 830, 453))
        self.scrollAreaContent.setMaximumSize(QSize(16777215, 16777215))
        self.scrollAreaContent.setObjectName("scrollAreaContent")
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaContent)
        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")

    def setLayoutes(self):
        self.scrollAreaLayout.addWidget(self.listGrid)
        self.scrollArea.setWidget(self.scrollAreaContent)

        self.layout.addWidget(self.scrollArea)

    def setListGrid(self):
        listGrid = ListWidget(self, self.ebookList)
        self.listGrid = listGrid

    def update(self):
        self.setEbookList()
        self.listGrid.update(self.ebookList)


class EbookPage(QWidget):

    def __init__(self, name, parent=None):
        super().__init__()
        self.nameString = name
        self.setObjectName("ebookPage")
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("ebookPageLayout")
        self.setTopBar()

        content = EbookPageContent(self, name)
        self.setContent(content)

        self.setLabels(name)
        self.setInputs()

        self.setLayoutes()

    def setTopBar(self):
        self.topbar = QFrame(self)
        self.topbar.setMaximumSize(QSize(16777215, 130))
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setObjectName("ebookPageTopbar")
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setContentsMargins(30, 50, 60, 10)
        self.topbarLayout.setSpacing(0)
        self.topbarLayout.setObjectName("ebookPageTopbarLayout")

    def setLabels(self, name):
        self.pageName = QLabel(self.topbar)
        self.pageName.setObjectName("ebookPageTitle")
        self.setPageName(name)

    def setInputs(self):
        self.search = QLineEdit(self.topbar)
        self.search.setMaximumSize(QSize(EBOOKPAGE_SEARCH_WIDTH, 16777215))
        self.search.setObjectName("ebookPageSearch")
        self.search.setPlaceholderText("Search")
        self.search.textChanged.connect(self.searchHandler)

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.pageName)
        self.topbarLayout.addWidget(self.search)

        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)

    def setContent(self, content):
        self.content = content

    def setPageName(self, name):
        name = "%s - %s" % (name, self.content.listGrid.count())
        self.pageName.setText(name)

    def searchHandler(self, text):
        self.content.listGrid.search(text)

    def update(self):
        self.content.update()
        self.setPageName(self.nameString)
