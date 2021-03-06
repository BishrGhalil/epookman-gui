#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.

from os import (getenv, path)

from PyQt5.QtCore import (QRect, QSize, Qt, QThread, pyqtSignal, QUrl)
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                             QListView, QListWidget, QMessageBox, QProgressBar,
                             QPushButton, QScrollArea, QVBoxLayout, QWidget,
                             QComboBox)

from epookman_gui.api.db import (commit_dir, commit_ebook, connect,
                                 commit_option, del_dir, del_ebooks,
                                 fetch_dirs)
from epookman_gui.api.dirent import Dirent
from epookman_gui.api.search import scaneOneByOne
from epookman_gui.api.db import (connect, fetch_option)

MAXIMUM_QT_NUMBER = 16777215
DIRS_LIST_HEIGHT = 200


class scaneThread(QThread):
    _currentValueSignal = pyqtSignal(int)
    _currentDirSignal = pyqtSignal(int)

    def __init__(self, dirs):
        super(scaneThread, self).__init__()
        self.dirs = dirs

    def run(self):

        conn = connect()
        totalDirs = len(self.dirs)
        for index, _dir in enumerate(self.dirs):
            dirPercent = int(((index) / (totalDirs)) * 100)
            self._currentDirSignal.emit(dirPercent)
            for percent, ebook in scaneOneByOne(_dir):
                if ebook:
                    commit_ebook(conn, ebook)

                self._currentValueSignal.emit(percent + 1)

        self._currentValueSignal.emit(100)
        self._currentDirSignal.emit(100)
        conn.close()


class Content(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("settingsContent")
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("settingsContentLayout")
        self.layout.setContentsMargins(30, 0, 30, 0)
        self.layout.setSpacing(10)

        self.dirs = {}

        self.setScrollArea()
        self.setDirsControleFrame()
        self.setProgressBarsFrame()
        self.setThemingFrame()
        self.setEbookReaderFrame()
        self.setEmptyFrame()

        self.setButtons()
        self.setProgressBars()
        self.setList()
        self.setThemingMenu()
        self.setLabels()
        self.setLayoutes()

    def setScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("settingsScrollarea")
        self.scrollArea.setMaximumSize(
            QSize(MAXIMUM_QT_NUMBER, DIRS_LIST_HEIGHT))

        self.scrollAreaContent = QWidget()
        self.scrollAreaContent.setMaximumSize(
            QSize(MAXIMUM_QT_NUMBER, DIRS_LIST_HEIGHT))
        self.scrollAreaContent.setObjectName("settingsScrollareaContent")
        self.scrollAreaLayout = QHBoxLayout(self.scrollAreaContent)
        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setObjectName("settingsContentScrollareaLayout")
        self.scrollAreaLayout.setAlignment(Qt.AlignTop)

    def setDirsControleFrame(self):
        self.dirsControleFrame = QFrame(self)
        self.dirsControleFrame.setFrameShape(QFrame.NoFrame)
        self.dirsControleFrameLayout = QHBoxLayout(self.dirsControleFrame)
        self.dirsControleFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.dirsControleFrameLayout.setSpacing(10)
        self.dirsControleFrameLayout.setAlignment(Qt.AlignTop)

    def setButtons(self):
        self.buttons = QFrame(self.dirsControleFrame)
        self.buttonsLayout = QVBoxLayout(self.buttons)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(5)
        self.buttonsLayout.setObjectName("settingsContentButtonsLayout")
        self.buttonsLayout.setAlignment(Qt.AlignTop)

        self.ebookReaderButton = QPushButton(self.buttons)
        default_reader = self.getDefaultEbookReader()
        self.ebookReaderButton.setText(f"{default_reader}, Click to change it")
        self.ebookReaderButton.clicked.connect(self.selectEbookReaderDialog)
        self.ebookReaderButton.setObjectName("scaneButton")
        self.ebookReaderButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ebookReaderButton.setMinimumSize(QSize(250, 50))

        self.scane = QPushButton(self.buttons)
        self.scane.setMinimumSize(QSize(MAXIMUM_QT_NUMBER, 50))
        self.scane.setObjectName("scaneButton")
        self.scane.setText("RESCANE")
        self.scane.setCursor(QCursor(Qt.PointingHandCursor))
        self.scane.clicked.connect(self.scaneUpdateProgressBar)

        self.addDir = QPushButton(self.buttons)
        self.addDir.setMinimumSize(QSize(MAXIMUM_QT_NUMBER, 50))
        self.addDir.setObjectName("addDirButton")
        self.addDir.setText("ADD DIR")
        self.addDir.setCursor(QCursor(Qt.PointingHandCursor))
        self.addDir.clicked.connect(self.addDirScane)

    def setProgressBarsFrame(self):
        self.progressBarsFrame = QFrame(self)
        self.progressBarsFrame.setObjectName("progressBarsFrame")
        self.progressBarsFrame.setFrameShape(QFrame.NoFrame)
        self.progressBarsFrame.setMaximumSize(QSize(MAXIMUM_QT_NUMBER, 80))
        self.progressBarsFrameLayout = QVBoxLayout(self.progressBarsFrame)
        self.progressBarsFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.progressBarsFrameLayout.setSpacing(5)
        self.progressBarsFrameLayout.setAlignment(Qt.AlignTop)

    def setThemingFrame(self):
        self.themingFrame = QFrame(self)
        self.themingFrame.setFrameShape(QFrame.NoFrame)
        self.themingFrame.setObjectName("themingFrame")
        self.themingFrameLayout = QHBoxLayout(self.themingFrame)
        self.themingFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.themingFrameLayout.setSpacing(10)
        self.themingFrameLayout.setAlignment(Qt.AlignTop)
        self.themingFrame.setMaximumSize(QSize(300, 40))

    def setEbookReaderFrame(self):
        self.ebookReaderFrame = QFrame(self)
        self.ebookReaderFrame.setFrameShape(QFrame.NoFrame)
        self.ebookReaderFrame.setObjectName("ebookReaderFrame")
        self.ebookReaderLayout = QHBoxLayout(self.ebookReaderFrame)
        self.ebookReaderLayout.setContentsMargins(0, 0, 0, 0)
        self.ebookReaderLayout.setSpacing(10)
        self.ebookReaderLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.ebookReaderFrame.setMaximumSize(QSize(500, 100))

    def getDefaultEbookReader(self):
        conn = connect()
        default_reader = fetch_option(conn, "DEFAULT_READER")
        conn.close()
        if not default_reader:
            default_reader = "None"
        else:
            default_reader = path.basename(default_reader)

        return default_reader

    def setEmptyFrame(self):
        self.emptyFrame = QFrame(self)
        self.emptyFrame.setFrameShape(QFrame.NoFrame)
        self.emptyFrame.setObjectName("ebookReaderFrame")

    def setLabels(self):
        self.themingLabel = QLabel(self.themingFrame)
        self.themingLabel.setObjectName("themingLabel")
        text = "Theme"
        self.themingLabel.setText(text)
        self.themingLabel.setMaximumSize(QSize(80, MAXIMUM_QT_NUMBER))

        self.ebookReaderLabel = QLabel(self.ebookReaderFrame)
        self.ebookReaderLabel.setObjectName("themingLabel")
        self.ebookReaderLabel.setText("Reader:")
        self.ebookReaderLabel.setMaximumSize(QSize(80, MAXIMUM_QT_NUMBER))

    def setThemingMenu(self):
        self.themes = [
            "black&white", "dark-purple", "dark-blue", "dark-red",
            "dark-yellow", "light-purple", "light-blue", "light-red",
            "light-yellow", "white&black"
        ]

        self.themingMenu = QComboBox(self.themingFrame)
        self.themingMenu.setMaximumSize(QSize(300, 100))
        conn = connect()
        default_theme = fetch_option(conn, "DEFAULT_THEME")
        conn.close()

        for theme in self.themes:
            self.themingMenu.addItem(theme)

        if not default_theme:
            index = 0
        else:
            index = self.themes.index(default_theme)

        self.themingMenu.setCurrentIndex(index)

    def selectEbookReaderDialog(self):
        appsPath = "/usr/bin"
        ebookReaderDialog = QFileDialog(None)
        ebookReaderDialog.setDirectory(appsPath)
        ebookReaderUrl = ebookReaderDialog.getOpenFileUrl()
        ebookReaderUrl = ebookReaderUrl[0].path()
        conn = connect()
        commit_option(conn, "DEFAULT_READER", ebookReaderUrl)
        conn.close()
        default_reader = self.getDefaultEbookReader()
        self.ebookReaderButton.setText(f"{default_reader}, Click to change it")

    def setProgressBars(self):
        self.vpbar = QProgressBar(self.progressBarsFrame)
        self.vpbar.setMinimumSize(QSize(100, 10))
        self.vpbar.setObjectName("valuesProgressbar")

        self.dpbar = QProgressBar(self.progressBarsFrame)
        self.dpbar.setMinimumSize(QSize(100, 10))
        self.dpbar.setObjectName("dirsProgressbar")
        self.dpbar.setFormat("%v/%m")

    def setList(self):
        self.list = QListWidget(self.dirsControleFrame)

        self.list.setAutoFillBackground(True)
        self.list.setViewMode(QListView.ListMode)
        self.list.setCursor(QCursor(Qt.PointingHandCursor))
        self.list.setSpacing(2)
        self.list.setMaximumSize(QSize(1300, DIRS_LIST_HEIGHT))
        self.list.setObjectName("dirsList")

        self.setListItems()
        self.list.itemDoubleClicked.connect(self.showDelDialog)

    def setLayoutes(self):
        self.progressBarsFrameLayout.addWidget(self.dpbar)
        self.progressBarsFrameLayout.addWidget(self.vpbar)

        self.buttonsLayout.addWidget(self.addDir)
        self.buttonsLayout.addWidget(self.scane)

        self.dirsControleFrameLayout.addWidget(self.list)
        self.dirsControleFrameLayout.addWidget(self.buttons)

        self.scrollAreaLayout.addWidget(self.dirsControleFrame)
        self.scrollArea.setWidget(self.scrollAreaContent)

        self.themingFrameLayout.addWidget(self.themingLabel)
        self.themingFrameLayout.addWidget(self.themingMenu)

        self.ebookReaderLayout.addWidget(self.ebookReaderLabel)
        self.ebookReaderLayout.addWidget(self.ebookReaderButton)

        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.progressBarsFrame)
        self.layout.addWidget(self.themingFrame)
        self.layout.addWidget(self.ebookReaderFrame)
        self.layout.addWidget(self.emptyFrame)

    def scaneUpdateProgressBar(self, dirs=None):
        if not dirs:
            if not self.dirs:
                return

            dirs = list(self.dirs.keys())

        self.dpbar.setFormat("%v/%m")
        self.vpbar.resetFormat()
        self.scane.setEnabled(False)
        self.addDir.setEnabled(False)
        self.thread = scaneThread(dirs)
        self.thread._currentValueSignal.connect(self.updateVProgressBar)
        self.thread._currentDirSignal.connect(self.updateDProgressBar)
        self.thread.start()

    def addDirScane(self):
        documentsPath = path.join(getenv("HOME"), "Documents")
        dirPath = QFileDialog.getExistingDirectory(None, "Choose A Directory",
                                                   documentsPath)
        if not dirPath:
            return

        conn = connect()
        Dir = Dirent(dirPath)
        commit_dir(conn, Dir)
        conn.close()
        self.updateList()
        self.scaneUpdateProgressBar((dirPath, ))

    def showDelDialog(self, item):
        msg = "Are you sure you want to delete this directory?\n" \
            "This action will also delete all ebooks that belong to this directory"

        func = lambda button: self.delDirUpdateList(button, item)
        self.showDialog(msg, func)

    def showDialog(self, text, func=None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if func:
            msgBox.buttonClicked.connect(lambda button: func(button))

        retval = msgBox.exec_()

    def delDirUpdateList(self, button, item):
        if button.text() != "OK":
            return

        conn = connect()
        dirPath = item.text()
        del_dir(conn, dirPath)
        del_ebooks(conn, directory=dirPath)
        self.dirs.pop(dirPath, None)
        conn.close()
        self.updateList()

    def setListItems(self):
        conn = connect()
        dirs = fetch_dirs(conn)
        conn.close()

        for _dir in dirs:
            self.dirs[_dir.path] = _dir
            self.list.addItem(_dir.path)

        if len(dirs) < 1:
            msg = "Start by adding some directories"
            self.list.addItem(msg)

    def updateList(self):
        self.list.clear()
        self.setListItems()

    def updateVProgressBar(self, msg):
        self.vpbar.setValue(int(msg))
        if self.vpbar.value() >= 99:
            self.vpbar.setValue(0)
            self.vpbar.setFormat("")

    def updateDProgressBar(self, msg):
        self.dpbar.setValue(int(msg))
        if self.dpbar.value() >= 99:
            self.dpbar.setValue(0)
            self.scane.setEnabled(True)
            self.addDir.setEnabled(True)
            self.dpbar.setFormat("")


class SettingsPage(QWidget):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("pageSettings")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("settings_layout")

        self.setTopbar()
        content = Content(self)
        self.setContent(content)
        self.setLabels()
        self.setLayoutes()

    def setTopbar(self):
        self.topbar = QFrame(self)
        self.topbar.setMaximumSize(QSize(MAXIMUM_QT_NUMBER, 130))
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setObjectName("settingsPage_topbar")
        self.topbarLayout = QHBoxLayout(self.topbar)
        self.topbarLayout.setContentsMargins(30, 40, 60, 10)
        self.topbarLayout.setSpacing(0)
        self.topbarLayout.setObjectName("settingsPage_topbar_layout")

    def setLabels(self):
        self.label = QLabel(self.topbar)
        self.label.setObjectName("settingsPageTitle")
        self.label.setText("SETTINGS")

    def setContent(self, content):
        self.content = content

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.label)
        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)
