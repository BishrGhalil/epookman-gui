#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
from PyQt5.QtWidgets import (QFrame, QGridLayout, QLabel)

from epookman.ui.widgets.ebook import (EBOOKFRAME_WIDTH, EbookFrame,
                                       EmbtyFrame)


class Grid(QFrame):

    def __init__(self, QParent, ebookList, parent=None):
        super().__init__(QParent)
        self.parent = parent
        self.cols = QParent.frameGeometry().width() * 10 // EBOOKFRAME_WIDTH
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("ebookpage_grid")
        self.layout = QGridLayout(self)
        self.layout.setObjectName("ebookpage_grid_layout")
        self.layout.setContentsMargins(0, 30, 0, 0)
        self.layout.setSpacing(30)

        self.set(ebookList)

    def set(self, ebookList):
        self.list = ebookList
        col = 0
        row = 0
        for ebook in ebookList:
            if type(ebook) == int:
                break
            if col == self.cols:
                row += 1
                col = 0
                continue

            col += 1

            ebookFrame = EbookFrame(self, ebook)
            self.layout.addWidget(ebookFrame, row, col)

        _len = len(ebookList)
        if _len < self.cols:
            row = 0
            for i in range(_len + 1, self.cols + 2):
                if i > self.cols:
                    row = 1
                self.layout.addWidget(EmbtyFrame(self), row, i)

    def delete(self):
        for cnt in reversed(range(self.layout.count())):
            widget = self.layout.takeAt(cnt).widget()

            if widget is not None:
                widget.deleteLater()

    def update(self, ebookList):
        self.delete()
        self.set(ebookList)
