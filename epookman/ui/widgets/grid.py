#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel
from epookman.ui.widgets.ebook import EbookFrame

EBOOK_PAGE_COLS = 6


class Grid(QFrame):

    def __init__(self, QParent, ebookList, parent=None):
        super().__init__(QParent)
        self.parent = parent
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("ebookpage_grid")
        self.layout = QGridLayout(self)
        self.layout.setObjectName("ebookpage_grid_layout")
        self.layout.setContentsMargins(0, 30, 0, 0)
        self.layout.setSpacing(30)

        self.set(ebookList)

    def set(self, ebookList):
        col = 0
        row = 0
        for ebook in ebookList:
            if col == EBOOK_PAGE_COLS:
                row += 1
                col = 0
                continue

            col += 1
            self.setEbookFrame(ebook)
            self.layout.addWidget(self.ebookFrame, row, col)

    def setEbookFrame(self, ebook):
        self.ebookFrame = EbookFrame(self, ebook)
