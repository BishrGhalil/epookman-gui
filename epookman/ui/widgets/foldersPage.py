#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QScrollArea, QVBoxLayout,
                             QWidget)


class Content(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("folders_content")
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("folders_content_layout")

    def setScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollarea = QWidget()
        self.scrollarea.setGeometry(QRect(0, 0, 862, 435))
        self.scrollarea.setObjectName("scrollarea")
        self.scrollareaLayout = QHBoxLayout(self.scrollarea)
        self.scrollareaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollareaLayout.setSpacing(0)
        self.scrollareaLayout.setObjectName("folders_content_scrollarea_layout")
        self.scrollArea.setWidget(self.scrollarea)

    def setLayoutes(self):
        self.layout.addWidget(self.scrollArea)


class FoldersPage(QWidget):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("pageFolders")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("folders_layout")

        content = Content(self)
        self.setContent(content)

    def setTopbar(self):
        self.topbar = QFrame(self)
        self.topbar.setMaximumSize(QSize(16777215, 70))
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setObjectName("topbar")
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setContentsMargins(30, 10, 30, 0)
        self.topbarLayout.setObjectName("folders_topbarLayout")

    def setLabels(self):
        self.label = QLabel(self.topbar)
        self.label.setObjectName("label")

    def setContent(self, content):
        self.content = content

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.label)
        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)
