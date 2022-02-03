#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

LEFTMENU_WIDTH = 120
LEFTMENU_HEIGHT = 16777215

LEFTMENU_LOGO_WIDTH = 120
LEFTMENU_LOGO_HEIGHT = 50


class LeftMenu(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("leftmenu")
        self.parent = parent
        self.setMinimumSize(QSize(LEFTMENU_WIDTH, LEFTMENU_HEIGHT))

        with open("epookman/ui/QSS/leftMenu.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("leftmenu_layout")

        self.setTopMenusFrame()
        self.setButtons()
        self.setLayoutes()

    def setTopMenusFrame(self):
        self.topMenus = QFrame(self)
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.topMenus.setObjectName("leftmenu_topmenus")
        self.topMenusLayout = QVBoxLayout(self.topMenus)
        self.topMenusLayout.setContentsMargins(0, 50, 0, 0)
        self.topMenusLayout.setSpacing(2)

    def setButtons(self):

        self.reading = QPushButton(self.topMenus)
        self.reading.setMinimumSize(QSize(0, 50))
        self.reading.setObjectName("leftmenu_button_reading")
        self.reading.setText("READING")
        self.reading.setCursor(QCursor(Qt.PointingHandCursor))

        self.toread = QPushButton(self.topMenus)
        self.toread.setMinimumSize(QSize(0, 50))
        self.toread.setObjectName("leftmenu_button_toread")
        self.toread.setText("TO READ")
        self.toread.setCursor(QCursor(Qt.PointingHandCursor))

        self.all = QPushButton(self.topMenus)
        self.all.setMinimumSize(QSize(0, 50))
        self.all.setObjectName("leftmenu_button_all")
        self.all.setText("ALL")
        self.all.setCursor(QCursor(Qt.PointingHandCursor))

        self.done = QPushButton(self.topMenus)
        self.done.setMinimumSize(QSize(0, 50))
        self.done.setObjectName("leftmenu_button_done")
        self.done.setText("DONE")
        self.done.setCursor(QCursor(Qt.PointingHandCursor))

        self.fav = QPushButton(self.topMenus)
        self.fav.setMinimumSize(QSize(0, 50))
        self.fav.setObjectName("leftmenu_button_fav")
        self.fav.setText("FAV")
        self.fav.setCursor(QCursor(Qt.PointingHandCursor))

        self.folders = QPushButton(self.topMenus)
        self.folders.setMinimumSize(QSize(0, 50))
        self.folders.setObjectName("leftmenu_button_folders")
        self.folders.setText("FOLDERS")
        self.folders.setCursor(QCursor(Qt.PointingHandCursor))

        self.settings = QPushButton(self.topMenus)
        self.settings.setMinimumSize(QSize(0, 50))
        self.settings.setObjectName("leftmenu_button_settings")
        self.settings.setText("SETTINGS")
        self.settings.setCursor(QCursor(Qt.PointingHandCursor))

    def setLayoutes(self):
        self.topMenusLayout.addWidget(self.folders)
        self.topMenusLayout.addWidget(self.reading)
        self.topMenusLayout.addWidget(self.toread)
        self.topMenusLayout.addWidget(self.done)
        self.topMenusLayout.addWidget(self.fav)
        self.topMenusLayout.addWidget(self.all)
        self.topMenusLayout.addWidget(self.settings)

        self.layout.addWidget(self.topMenus, 0, Qt.AlignTop)
