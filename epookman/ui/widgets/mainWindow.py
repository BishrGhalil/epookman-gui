#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget
from epookman.ui.widgets.leftMenu import LeftMenu
from epookman.ui.widgets.pages import Pages

MAINWINDOW_WIDTH_MIN = 1000
MAINWINDOW_HEIGHT_MIN = 500

MAINWINDOW_WIDTH = 1400
MAINWINDOW_HEIGHT = 700

DEFAULT_PAGE = "ALL"


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.setupMainWindow(MainWindow)

    def setupMainWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MAINWINDOW_WIDTH, MAINWINDOW_HEIGHT)
        MainWindow.setMinimumSize(
            QSize(MAINWINDOW_WIDTH_MIN, MAINWINDOW_HEIGHT_MIN))
        with open("epookman/ui/QSS/mainWindow.qss", "r") as f:
            MainWindow.setStyleSheet(f.read())
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
        self.setDefaultPage()

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

        button = self.leftMenu.folders
        self.connectButton(button, leftMenufunc, "FOLDERS")

        button = self.leftMenu.settings
        self.connectButton(button, leftMenufunc, "SETTINGS")

    def connectButton(self, button, func, *args):
        button.setMouseTracking(True)
        button.mousePressEvent = lambda event: func(*args)

    def retranslateUi(self, MainWindow):
        _translate = translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p align=\"center\"><span style=\" font-size:15pt;\">EPOOKMAN</span></p></body></html>"
            ))

    def setDefaultPage(self):
        self.pages.changePage(DEFAULT_PAGE)
