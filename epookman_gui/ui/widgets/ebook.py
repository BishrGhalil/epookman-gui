#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

import subprocess
from os import getenv, path

from PyQt5.QtCore import (QRect, QSize, Qt)
from PyQt5.QtGui import (QBrush, QCursor, QIcon, QPalette, QPixmap)
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QListWidgetItem, QMenu)

from epookman_gui.api.db import DB_PATH, commit_ebook, connect
from epookman_gui.api.ebook import (STATUS_HAVE_READ, STATUS_HAVE_NOT_READ,
                                STATUS_READING)
from epookman_gui.api.thumbnailer import thumbnailer

FRAME_SCALE = 2
QUALITY_SCALE = 3

FONT_HEIGHT = 30

THUMBNAIL_WIDTH = 99 * FRAME_SCALE
THUMBNAIL_HEIGHT = 128 * FRAME_SCALE

EBOOKFRAME_WIDTH = THUMBNAIL_WIDTH
EBOOKFRAME_HEIGHT = THUMBNAIL_HEIGHT + FONT_HEIGHT

THUMBNAILS_DIR = path.join(getenv("HOME"), ".cache", "epookman-gui",
                           "thumbnails")


class Button(QPushButton):

    def __init__(self,
                 name,
                 state,
                 iconPath,
                 tootip,
                 func,
                 QParent,
                 parent=None):
        super().__init__(QParent)

        self.setSize()
        self.setObjectName(name)
        self.iconFormat = ".xpm"
        self.state = state
        self.name = name

        self.iconPath = path.join(iconPath, name) + self.iconFormat
        self.iconDisabledPath = path.join(iconPath,
                                          name) + "Disabled" + self.iconFormat

        self.setIconByState()
        self.setToolTip(tootip)

        self.setMouseTracking(True)
        self.setClickFunction(func)

    def toggleState(self):
        self.state = not self.state
        self.setIconByState()

    def disable(self):
        self.state = False
        self.setIconByState()

    def enable(self):
        self.state = True
        self.setIconByState()

    def setSize(self):

        self.setMaximumSize(QSize(BUTTONS_ICON, BUTTONS_ICON))

    def setIconByState(self):

        if self.state:
            icon = QIcon(self.iconPath)
        else:
            icon = QIcon(self.iconDisabledPath)
        self.setIcon(icon)
        self.setIconSize(QSize(BUTTONS_ICON // 2, BUTTONS_ICON // 2))

    def setClickFunction(self, func, *args):
        self.mousePressEvent = lambda event: func(self, *args, event)


class EbookItem(QListWidgetItem):

    def __init__(self, QParent, ebook, parent=None):
        super().__init__(QParent)
        self.parent = parent
        self.ebook = ebook

        self.setText(ebook.name)
        self.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.setToolTip(ebook.name)
        self.setThumbnail()
        self.setSizeHint(QSize(EBOOKFRAME_WIDTH, EBOOKFRAME_HEIGHT))

    def hide(self):
        self.setHidden(True)

    def show(self):
        self.setHidden(False)

    def setThumbnail(self):

        self.thumbnail_file = path.join(THUMBNAILS_DIR,
                                        self.ebook.name + ".png")

        img = QPixmap(self.thumbnail_file)
        if img.isNull():
            img = QPixmap("epookman_gui/ui/resources/document.png")

        img = img.scaled(THUMBNAIL_WIDTH * QUALITY_SCALE,
                         THUMBNAIL_HEIGHT * QUALITY_SCALE)

        self.setIcon(QIcon(img))
