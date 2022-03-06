#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.

from PyQt5.QtCore import (QCoreApplication, QSize)
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QWidget,
                             QMessageBox)
from epookman_gui.ui.widgets.leftMenu import LeftMenu
from epookman_gui.ui.widgets.pages import Pages
from epookman_gui.api.themer import themer
from epookman_gui.api.db import (fetch_option, commit_option, connect)

MAINWINDOW_WIDTH_MIN = 1000
MAINWINDOW_HEIGHT_MIN = 500

MAINWINDOW_WIDTH = 1400
MAINWINDOW_HEIGHT = 700

DEFAULT_PAGE = "ALL"
DEFAULT_THEME = "dark-purple"


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.setupMainWindow(MainWindow)

    def setupMainWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MAINWINDOW_WIDTH, MAINWINDOW_HEIGHT)
        MainWindow.setMinimumSize(
            QSize(MAINWINDOW_WIDTH_MIN, MAINWINDOW_HEIGHT_MIN))
        styleSheet = self.getDefaultStyle()
        MainWindow.setStyleSheet(styleSheet)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.MainWindowLayout = QVBoxLayout(self.centralwidget)
        self.MainWindowLayout.setContentsMargins(0, 0, 0, 0)
        self.MainWindowLayout.setSpacing(0)
        self.MainWindowLayout.setObjectName("MainWindowLayout")

        self.MainWindowContent = QFrame(self.centralwidget)
        self.MainWindowContent.setFrameShape(QFrame.NoFrame)
        self.MainWindowContent.setFrameShadow(QFrame.Raised)
        self.MainWindowContent.setObjectName("MainWindowContent")
        self.MainWindowContentLayout = QHBoxLayout(self.MainWindowContent)
        self.MainWindowContentLayout.setContentsMargins(0, 0, 0, 0)
        self.MainWindowContentLayout.setSpacing(0)
        self.MainWindowContentLayout.setObjectName("MainWindowContentLayout")

        self.leftMenu = LeftMenu(MainWindow)
        self.pages = Pages(MainWindow)

        self.MainWindowContentLayout.addWidget(self.leftMenu)
        self.MainWindowContentLayout.addWidget(self.pages)

        self.MainWindowLayout.addWidget(self.MainWindowContent)
        MainWindow.setCentralWidget(self.centralwidget)

        self.setButtons()
        self.connectThemingMenu()
        if self.pages.settingsPage.content.dirs:
            self.setDefaultPage("ALL")
        else:
            self.setDefaultPage("SETTINGS")

    def setButtons(self):
        # LEFT MENU BUTTONS
        leftMenufunc = self.pages.changePage

        button = self.leftMenu.reading
        self.connectButton(button, leftMenufunc, "READING")

        button = self.leftMenu.toread
        self.connectButton(button, leftMenufunc, "TO READ")

        button = self.leftMenu.all
        self.connectButton(button, leftMenufunc, "ALL")

        button = self.leftMenu.done
        self.connectButton(button, leftMenufunc, "DONE")

        button = self.leftMenu.fav
        self.connectButton(button, leftMenufunc, "FAV")

        button = self.leftMenu.settings
        self.connectButton(button, leftMenufunc, "SETTINGS")

    def connectButton(self, button, func, *args):
        button.setMouseTracking(True)
        button.mousePressEvent = lambda event: func(*args)

    def connectThemingMenu(self):
        self.pages.settingsPage.content.themingMenu.currentTextChanged.connect(
            self.changeTheme)

    def changeTheme(self, theme):
        conn = connect()
        commit_option(conn, "DEFAULT_THEME", theme)
        conn.close()
        styleSheet = themer(theme)
        self.centralwidget.setStyleSheet(styleSheet)

    def getDefaultStyle(self):
        conn = connect()
        theme = fetch_option(conn, "DEFAULT_THEME")
        if not theme:
            theme = DEFAULT_THEME

        self.theme = theme
        styleSheet = themer(theme)
        conn.close()
        return styleSheet

    def retranslateUi(self, MainWindow):
        _translate = translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def setDefaultPage(self, name=None):
        if not name:
            name = DEFAULT_PAGE
        self.pages.changePage(name)
