#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtCore import (QSize, Qt, QRect, QEasingCurve, QPropertyAnimation)
from PyQt5.QtGui import (QCursor, QIcon, QPixmap)
from PyQt5.QtWidgets import (QFrame, QPushButton, QVBoxLayout, QWidget)

LEFTMENU_WIDTH = 120
LEFTMENU_HEIGHT = 16777215

LEFTMENU_MINIMIZED_WIDTH = 50
LEFTMENU_BUTTON_HEIGHT = 50
LEFTMENU_BUTTON_WIDTH = 0

LEFTMENU_TOGGLE_ICON = 25

LEFTMENU_EXTENDED = False


class LeftMenu(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("leftmenu")
        self.parent = parent
        self.setMinimumSize(QSize(LEFTMENU_MINIMIZED_WIDTH, LEFTMENU_HEIGHT))

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("leftmenuLayout")

        self.setTopMenusFrame()
        self.setButtons()
        self.setLayoutes()
        self.setAnimations()
        self.toggleButtonsVisbilaty(LEFTMENU_EXTENDED)

    def setTopMenusFrame(self):
        self.topMenus = QFrame(self)
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.topMenus.setObjectName("leftmenuTopmenus")
        self.topMenusLayout = QVBoxLayout(self.topMenus)
        self.topMenusLayout.setContentsMargins(0, 0, 0, 0)
        self.topMenusLayout.setSpacing(2)

    def setButtons(self):

        self.toggle = QPushButton(self.topMenus)
        self.toggle.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.toggle.setObjectName("leftmenuButtonToggle")
        icon = QIcon("epookman_gui/ui/resources/toggle.png")
        self.toggle.setIcon(icon)
        self.toggle.setIconSize(
            QSize(LEFTMENU_TOGGLE_ICON, LEFTMENU_TOGGLE_ICON))
        self.toggle.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle.clicked.connect(self.toggleAnimate)

        self.reading = QPushButton(self.topMenus)
        self.reading.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.reading.setObjectName("leftmenuButton")
        self.reading.setText("READING")
        self.reading.setCursor(QCursor(Qt.PointingHandCursor))
        self.reading.setToolTip("Currently Reading Books")

        self.toread = QPushButton(self.topMenus)
        self.toread.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.toread.setObjectName("leftmenuButton")
        self.toread.setText("TO READ")
        self.toread.setCursor(QCursor(Qt.PointingHandCursor))
        self.toread.setToolTip("Books To Read")

        self.all = QPushButton(self.topMenus)
        self.all.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.all.setObjectName("leftmenuButton")
        self.all.setText("ALL")
        self.all.setCursor(QCursor(Qt.PointingHandCursor))
        self.all.setToolTip("Books To Read")

        self.done = QPushButton(self.topMenus)
        self.done.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.done.setObjectName("leftmenuButton")
        self.done.setText("DONE")
        self.done.setCursor(QCursor(Qt.PointingHandCursor))
        self.done.setToolTip("Done Reading Books")

        self.fav = QPushButton(self.topMenus)
        self.fav.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.fav.setObjectName("leftmenuButton")
        self.fav.setText("FAV")
        self.fav.setCursor(QCursor(Qt.PointingHandCursor))
        self.fav.setToolTip("My Favorites Books")

        self.folders = QPushButton(self.topMenus)
        self.folders.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.folders.setObjectName("leftmenuButton")
        self.folders.setText("FOLDERS")
        self.folders.setCursor(QCursor(Qt.PointingHandCursor))
        self.folders.setToolTip("Browse Books By Folders")

        self.settings = QPushButton(self.topMenus)
        self.settings.setMinimumSize(
            QSize(LEFTMENU_BUTTON_WIDTH, LEFTMENU_BUTTON_HEIGHT))
        self.settings.setObjectName("leftmenuButton")
        self.settings.setText("SETTINGS")
        self.settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings.setToolTip("App settings")

        self.buttons = (self.all, self.fav, self.settings, self.folders,
                        self.done, self.reading, self.toread)

    def setLayoutes(self):
        self.topMenusLayout.addWidget(self.toggle)
        self.topMenusLayout.addWidget(self.all)
        self.topMenusLayout.addWidget(self.folders)
        self.topMenusLayout.addWidget(self.reading)
        self.topMenusLayout.addWidget(self.toread)
        self.topMenusLayout.addWidget(self.fav)
        self.topMenusLayout.addWidget(self.done)
        self.topMenusLayout.addWidget(self.settings)

        self.layout.addWidget(self.topMenus, 0, Qt.AlignTop)

    def setAnimations(self):
        self.widthAnimation = QPropertyAnimation(self, b"minimumWidth")
        self.widthAnimation.setDuration(150)
        self.widthAnimation.setEasingCurve(QEasingCurve.InOutQuart)

    def toggleAnimate(self):
        width = self.width()

        if width < LEFTMENU_WIDTH:
            newWidth = LEFTMENU_WIDTH
            visible = True
        else:
            newWidth = LEFTMENU_MINIMIZED_WIDTH
            visible = False

        self.toggleButtonsVisbilaty(visible)

        self.widthAnimation.setStartValue(width)
        self.widthAnimation.setEndValue(newWidth)
        self.widthAnimation.start()

    def toggleButtonsVisbilaty(self, visible):
        for button in self.buttons:
            button.setVisible(visible)
