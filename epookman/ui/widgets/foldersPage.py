#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QScrollArea, QVBoxLayout,
                             QWidget, QLabel)


class Content(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("folders_content")
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("folders_content_layout")
        self.layout.setContentsMargins(30, 0, 30, 0)

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
        self.scrollareaLayout.setObjectName(
            "folders_content_scrollarea_layout")
        self.scrollArea.setWidget(self.scrollarea)

    def setLayoutes(self):
        self.layout.addWidget(self.scrollArea)

    def setButtons(self):
        pass


class FoldersPage(QWidget):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("pageFolders")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("folders_layout")
        with open("epookman/ui/QSS/foldersPage.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setTopbar()
        content = Content(self)
        self.setContent(content)
        self.setLabels()
        self.setLayoutes()

    def setTopbar(self):
        self.topbar = QFrame(self)
        self.topbar.setMaximumSize(QSize(16777215, 130))
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setObjectName("settingsPage_topbar")
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setContentsMargins(30, 40, 60, 10)
        self.topbarLayout.setSpacing(0)
        self.topbarLayout.setObjectName("settingsPage_topbar_layout")

    def setLabels(self):
        self.label = QLabel(self.topbar)
        self.label.setObjectName("label")
        self.label.setText("FOLDERS")

    def setContent(self, content):
        self.content = content

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.label)
        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)
