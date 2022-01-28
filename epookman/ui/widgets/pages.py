#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtWidgets import (QFrame, QStackedWidget, QVBoxLayout)

from epookman.ui.widgets.ebookPage import EbookPage
from epookman.ui.widgets.foldersPage import FoldersPage


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
        self.stack = QStackedWidget(self)
        self.stack.setObjectName("pages_stack")

        ebookPage = EbookPage(self)
        folderPage = FoldersPage(self)
        self.setEbookPage(ebookPage)
        self.setFolderPage(folderPage)

        self.stack.addWidget(self.ebookPage)
        self.stack.addWidget(self.foldersPage)

        self.layout.addWidget(self.stack)

    def setEbookPage(self, ebookPage):
        self.ebookPage = ebookPage

    def setFolderPage(self, folderPage):
        self.foldersPage = folderPage
