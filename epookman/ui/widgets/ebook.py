#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

from os import path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout)

EBOOKFRAME_THUMBNAIL_WIDTH = 99 * 2
EBOOKFRAME_THUMBNAIL_HEIGHT = 128 * 2

EBOOKFRAME_WIDTH = EBOOKFRAME_THUMBNAIL_WIDTH
EBOOKFRAME_HEIGHT = EBOOKFRAME_THUMBNAIL_HEIGHT + 100

EBOOKFRAME_WIDTH_MIN = EBOOKFRAME_THUMBNAIL_WIDTH
EBOOKFRAME_HEIGHT_MIN = EBOOKFRAME_THUMBNAIL_HEIGHT + 100

EBOOKFRAME_TOOLBAR_HEIGHT = 42

EBOOKFRAME_BUTTONS_ICON = 40
EBOOKFRAME_BUTTONS_HEIGHT = EBOOKFRAME_BUTTONS_ICON
EBOOKFRAME_BUTTONS_WIDTH = EBOOKFRAME_WIDTH


class Button(QPushButton):

    def __init__(self, name, iconPath, tootip, func, QParent, parent=None):
        super().__init__(QParent)
        self.setMaximumSize(
            QSize(EBOOKFRAME_BUTTONS_ICON, EBOOKFRAME_BUTTONS_ICON))
        self.setObjectName(name)

        self.name = name
        self.iconPath = iconPath
        self.iconFormat = ".xpm"

        icon = QIcon(path.join(iconPath, name) + self.iconFormat)
        self.setIcon(icon)
        self.setIconSize(
            QSize(EBOOKFRAME_BUTTONS_ICON // 2, EBOOKFRAME_BUTTONS_ICON // 2))

        self.setToolTip(tootip)

        #  self.clicked.connect(func)

        self.setMouseTracking(True)
        self.mousePressEvent = lambda event: func(self, event)

        self.state = True

    def toggleState(self):
        self.state = not self.state


class EbookFrame(QFrame):

    def __init__(self, QParent, ebook, parent=None):
        super().__init__(QParent)
        self.parent = parent

        self.ebook = ebook
        self.setMinimumSize(QSize(EBOOKFRAME_WIDTH_MIN, EBOOKFRAME_HEIGHT_MIN))
        self.setMaximumSize(QSize(EBOOKFRAME_WIDTH, EBOOKFRAME_HEIGHT))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("ebook_%s" % self.ebook.name)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("ebook_layout_%s" % self.ebook.name)

        self.setThumbnail()
        self.setToolbar()
        self.setLabels()
        self.setButtons()
        self.setLayoutes()

        self.installEventFilter(self)

    def setThumbnail(self):
        self.thumbnail = QFrame(self)
        self.thumbnail.setMouseTracking(True)
        self.thumbnail.mousePressEvent = lambda event: self.openEbook(event)

        with open("epookman/ui/QSS/ebookFrameThumbnail.qss", "r") as f:
            self.thumbnail.setStyleSheet(f.read())

        self.thumbnail.setMaximumSize(
            QSize(EBOOKFRAME_THUMBNAIL_WIDTH, EBOOKFRAME_THUMBNAIL_HEIGHT))
        self.thumbnail.setLayoutDirection(Qt.LeftToRight)
        self.thumbnail.setToolTip(self.ebook.get_meta_data_string())
        self.thumbnail.setFrameShape(QFrame.NoFrame)
        self.thumbnail.setFrameShadow(QFrame.Raised)
        self.thumbnail.setObjectName("ebook_thumbnail_%s" % self.ebook.name)

    def setToolbar(self):
        self.toolbar = QFrame(self)
        self.toolbar.setMaximumSize(QSize(16777215, EBOOKFRAME_TOOLBAR_HEIGHT))

        with open("epookman/ui/QSS/ebookFrameToolbar.qss", "r") as f:
            self.toolbar.setStyleSheet(f.read())

        self.toolbar.setFrameShape(QFrame.NoFrame)
        self.toolbar.setFrameShadow(QFrame.Raised)
        self.toolbar.setObjectName("ebook_toolbar_%s" % self.ebook.name)
        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setObjectName("ebook_toolbar_layout_%s" %
                                         self.ebook.name)

    def setLabels(self):
        self.label = QLabel(self.toolbar)
        self.label.setObjectName("labelEbookname_%s" % self.ebook.name)
        self.label.setText(self.ebook.name)

    def setButtons(self):
        # == Making buttons frame ==
        self.buttons = QFrame(self)
        self.buttons.setMaximumSize(
            QSize(EBOOKFRAME_BUTTONS_WIDTH, EBOOKFRAME_BUTTONS_HEIGHT))
        self.buttons.setFrameShape(QFrame.NoFrame)
        self.buttons.setFrameShadow(QFrame.Raised)
        self.buttons.setObjectName("ebook_buttons_%s" % self.ebook.name)
        self.buttons.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout = QHBoxLayout(self.buttons)
        self.buttonsLayout.setObjectName("ebook_buttons_layout_%s" %
                                         self.ebook.name)

        # == Making buttons ==
        # To_Read button
        self.toread = Button("toread", "epookman/ui/resources",
                             "Mark as `To Read`", self.markToread,
                             self.buttons)

        # Fav button
        self.fav = Button("fav", "epookman/ui/resources", "Add to Fav",
                          self.markFav, self.buttons)
        # Done button
        self.done = Button("done", "epookman/ui/resources", "Mark as `Done`",
                           self.markDone, self.buttons)

    def setLayoutes(self):
        self.toolbarLayout.addWidget(self.label)

        self.buttonsLayout.addWidget(self.toread)
        self.buttonsLayout.addWidget(self.fav)
        self.buttonsLayout.addWidget(self.done)

        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.thumbnail)
        self.layout.addWidget(self.toolbar)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def openEbook(self, event):
        if event.button() == Qt.LeftButton:
            print("Openning Ebook: %s" % self.ebook.get_path())

    def markToread(self, button, event):
        self.ebook.set_status("have_not_read")

        self.toggleIcon(button, event)

    def markFav(self, button, event):
        self.ebook.toggle_fav()

        self.toggleIcon(button, event)

    def markDone(self, button, event):
        self.ebook.set_status("have_read")

        self.toggleIcon(button, event)

    def toggleIcon(self, button, event):
        button.toggleState()

        if not button.state:
            iconPath = path.join(button.iconPath,
                                 button.name) + "Disabled" + button.iconFormat
            icon = QIcon(iconPath)
        else:
            iconPath = path.join(button.iconPath,
                                 button.name) + button.iconFormat
            icon = QIcon(iconPath)

        button.setIcon(icon)
        super().eventFilter(button, event)
