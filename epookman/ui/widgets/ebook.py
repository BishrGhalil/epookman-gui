#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

import subprocess
from os import getenv, path

from PyQt5.QtCore import (QRect, QSize, Qt)
from PyQt5.QtGui import (QBrush, QCursor, QIcon, QPalette, QPixmap)
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QListWidgetItem, QMenu)

from epookman.api.db import DB_PATH, commit_ebook, connect
from epookman.api.ebook import Ebook
from epookman.api.thumbnailer import thumbnailer

SCALE = 2
PADDING_LR = 0
PADDING_TB = 0
EBOOKFRAME_THUMBNAIL_WIDTH = 99 * SCALE
EBOOKFRAME_THUMBNAIL_HEIGHT = 128 * SCALE

EBOOKFRAME_WIDTH = EBOOKFRAME_THUMBNAIL_WIDTH + PADDING_LR
EBOOKFRAME_HEIGHT = EBOOKFRAME_THUMBNAIL_HEIGHT + PADDING_TB

EBOOKFRAME_BUTTONS_ICON = 40
EBOOKFRAME_BUTTONS_HEIGHT = EBOOKFRAME_BUTTONS_ICON
EBOOKFRAME_BUTTONS_WIDTH = EBOOKFRAME_WIDTH

EBOOKFRAME_WIDTH_MIN = EBOOKFRAME_THUMBNAIL_WIDTH
EBOOKFRAME_HEIGHT_MIN = EBOOKFRAME_THUMBNAIL_HEIGHT + EBOOKFRAME_BUTTONS_HEIGHT
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

        self.setMaximumSize(
            QSize(EBOOKFRAME_BUTTONS_ICON, EBOOKFRAME_BUTTONS_ICON))

    def setIconByState(self):

        if self.state:
            icon = QIcon(self.iconPath)
        else:
            icon = QIcon(self.iconDisabledPath)
        self.setIcon(icon)
        self.setIconSize(
            QSize(EBOOKFRAME_BUTTONS_ICON // 2, EBOOKFRAME_BUTTONS_ICON // 2))

    def setClickFunction(self, func, *args):
        self.mousePressEvent = lambda event: func(self, *args, event)


class EbookListWidgetItem(QListWidgetItem):

    def __init__(self, QParent, ebook, parent=None):
        super().__init__(QParent)
        self.parent = parent
        self.ebook = ebook

        self.setText(ebook.name)
        self.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.setToolTip(ebook.name)
        self.setSizeHint(QSize(EBOOKFRAME_WIDTH, EBOOKFRAME_HEIGHT + 70))

    def hide(self):
        self.setHidden(True)

    def show(self):
        self.setHidden(False)


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
        self.setButtons()
        self.setLayoutes()

        self.installEventFilter(self)
        self.mousePressEvent = lambda event: self.openEbook(event, ebook)
        self.name = ebook.name

    def createThumbnail(self):
        self.thumbnail_file = path.join(THUMBNAILS_DIR,
                                        self.ebook.name + ".png")

        if not path.lexists(self.thumbnail_file):
            if thumbnailer(self.ebook.path,
                           path.join(THUMBNAILS_DIR, self.ebook.name)) == 0:
                return True
            else:
                return False

        else:
            return True

    def setThumbnail(self):
        self.thumbnail = QFrame(self)

        self.thumbnail.setMaximumSize(
            QSize(EBOOKFRAME_THUMBNAIL_WIDTH, EBOOKFRAME_THUMBNAIL_HEIGHT))
        self.thumbnail.setLayoutDirection(Qt.LeftToRight)
        self.thumbnail.setToolTip(self.ebook.metadata)
        self.thumbnail.setFrameShape(QFrame.NoFrame)
        self.thumbnail.setFrameShadow(QFrame.Raised)
        self.thumbnail.setObjectName("ebook_thumbnail_%s" % self.ebook.name)

        if self.createThumbnail():
            img = QPixmap(self.thumbnail_file)
        else:
            img = QPixmap("epookman/ui/resources/document.png")

        label = QLabel(self.thumbnail)
        img = img.scaled(EBOOKFRAME_THUMBNAIL_WIDTH,
                         EBOOKFRAME_THUMBNAIL_HEIGHT)
        label.setPixmap(img)

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
        buttonState = False
        if self.ebook.status == Ebook.STATUS_HAVE_NOT_READ:
            buttonState = True
        self.toread = Button("toread", buttonState, "epookman/ui/resources",
                             "Mark as To Read", self.markToread, self.buttons)

        # Fav button
        buttonState = False
        if self.ebook.fav:
            buttonState = True
        self.fav = Button("fav", buttonState, "epookman/ui/resources",
                          "Add to Fav", self.markFav, self.buttons)

        # Done button
        buttonState = False
        if self.ebook.status == Ebook.STATUS_HAVE_READ:
            buttonState = True
        self.done = Button("done", buttonState, "epookman/ui/resources",
                           "Mark as Done", self.markDone, self.buttons)

    def setLayoutes(self):

        self.buttonsLayout.addWidget(self.toread)
        self.buttonsLayout.addWidget(self.fav)
        self.buttonsLayout.addWidget(self.done)

        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.thumbnail)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def markToread(self, button, event):
        if self.ebook.status == Ebook.STATUS_HAVE_READ:
            self.toggleIcon(self.done, False)

        self.toggleIcon(button, True)
        self.ebook.set_status(Ebook.STATUS_HAVE_NOT_READ)
        self.commit()

        self.updateFrame(event)

    def markFav(self, button, event):
        state = True if not button.state else False
        self.toggleIcon(button, state)
        self.ebook.toggle_fav()
        self.commit()

        self.updateFrame(event)

    def markDone(self, button, event):
        if self.ebook.status == Ebook.STATUS_HAVE_NOT_READ:
            self.toggleIcon(self.toread, False)

        self.toggleIcon(button, True)
        self.ebook.set_status(Ebook.STATUS_HAVE_READ)
        self.commit()

        self.updateFrame(event)

    def toggleIcon(self, button, status):
        if status:
            button.enable()
        else:
            button.disable()

    def updateInfo(self):
        self.thumbnail.setToolTip(self.ebook.metadata)

    def updateFrame(self, event):
        self.updateInfo()
        super().eventFilter(self, event)

    def commit(self):
        conn = connect(DB_PATH)
        commit_ebook(conn, self.ebook)
        conn.commit()
        conn.close()

    def hide(self):
        for w in [self, self.buttons, self.thumbnail]:
            w.setVisible(False)

    def show(self):
        for w in [self, self.buttons, self.thumbnail]:
            w.setVisible(True)

    def openEbook(self, event, ebook):

        if event.button() == Qt.LeftButton:
            ereader = "zathura"
            file = open("/dev/null", "w")
            subprocess.Popen([ereader, ebook.get_path()], stderr=file)
            file.close()
