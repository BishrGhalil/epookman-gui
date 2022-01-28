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

MAINWINDOW_WIDTH = 1000
MAINWINDOW_HEIGHT = 500


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

    def setButtons(self):
        # LEFT MENU BUTTONS
        leftMenufunc = self.pages.ebookPage.setPageName

        readingBtn = self.leftMenu.reading
        self.connectButton(readingBtn, leftMenufunc, "READING")

        toreadBtn = self.leftMenu.toread
        self.connectButton(toreadBtn, leftMenufunc, "TO READ")

        allBtn = self.leftMenu.all
        self.connectButton(allBtn, leftMenufunc, "ALL")

        doneBtn = self.leftMenu.done
        self.connectButton(doneBtn, leftMenufunc, "DONE")

        favBtn = self.leftMenu.fav
        self.connectButton(favBtn, leftMenufunc, "FAV")

        foldersBtn = self.leftMenu.folders
        self.connectButton(foldersBtn, leftMenufunc, "FOLDERS")

    def connectButton(self, button, func, *args):
        button.clicked.connect(lambda: func(*args))

    def retranslateUi(self, MainWindow):
        _translate = translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p align=\"center\"><span style=\" font-size:15pt;\">EPOOKMAN</span></p></body></html>"
            ))
