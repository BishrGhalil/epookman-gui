#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import getenv, path

from PyQt5.QtCore import (QRect, QSize, Qt, QThread, pyqtSignal)
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                             QListView, QListWidget, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget, QProgressBar)

from epookman.api.db import (DB_PATH, commit_dir, commit_ebook, connect,
                             fetch_dirs)
from epookman.api.dirent import Dirent
from epookman.api.search import searchOneByOne


class scaneThread(QThread):
    _currentValueSignal = pyqtSignal(int)
    _currentDirSignal = pyqtSignal(int)

    def __init__(self, dirs):
        super(scaneThread, self).__init__()
        self.dirs = dirs

    def run(self):

        conn = connect(DB_PATH)
        totalDirs = len(self.dirs)
        for index, _dir in enumerate(self.dirs):
            for percent, ebook in searchOneByOne(_dir):
                if ebook:
                    commit_ebook(conn, ebook)

                dirPercent = int((100 * index + 1) / totalDirs)
                self._currentDirSignal.emit(dirPercent)
                self._currentValueSignal.emit(percent)

        self._currentValueSignal.emit(100)
        self._currentDirSignal.emit(100)
        conn.close()


class Content(QFrame):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("settings_content")
        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("settings_content_layout")
        self.layout.setContentsMargins(30, 0, 30, 0)

        self.dirs = []

        self.setScrollArea()
        self.setDirsControleFrame()
        self.setScaneFrame()
        self.setButtons()
        self.setProgressBars()
        self.setList()
        self.setLayoutes()

    def setScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("settings_scrollarea")

        self.scrollAreaContent = QWidget()
        self.scrollAreaContent.setObjectName("settings_scrollarea_content")
        self.scrollAreaLayout = QHBoxLayout(self.scrollAreaContent)
        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setObjectName(
            "settings_content_scrollarea_layout")

    def setLayoutes(self):
        self.scaneFrameLayout.addWidget(self.scane)
        self.scaneFrameLayout.addWidget(self.dpbar)
        self.scaneFrameLayout.addWidget(self.vpbar)

        self.buttonsLayout.addWidget(self.addDir)
        self.buttonsLayout.addWidget(self.delDir)

        self.dirsControleFrameLayout.addWidget(self.list)
        self.dirsControleFrameLayout.addWidget(self.buttons)

        self.scrollAreaLayout.addWidget(self.dirsControleFrame)

        self.scrollArea.setWidget(self.scrollAreaContent)

        self.layout.addWidget(self.scaneFrame)
        self.layout.addWidget(self.scrollArea)

    def setScaneFrame(self):
        self.scaneFrame = QFrame(self)
        self.scaneFrameLayout = QVBoxLayout(self.scaneFrame)
        self.scaneFrameLayout.setContentsMargins(0, 0, 0, 10)
        self.scaneFrameLayout.setSpacing(5)
        self.scaneFrameLayout.setAlignment(Qt.AlignTop)

    def setDirsControleFrame(self):
        self.dirsControleFrame = QFrame(self)
        self.dirsControleFrameLayout = QHBoxLayout(self.dirsControleFrame)
        self.dirsControleFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.dirsControleFrameLayout.setSpacing(10)
        self.dirsControleFrameLayout.setAlignment(Qt.AlignTop)

    def setButtons(self):
        self.buttons = QFrame(self.dirsControleFrame)
        self.buttonsLayout = QVBoxLayout(self.buttons)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setSpacing(5)
        self.buttonsLayout.setObjectName("settings_content_buttons_layout")
        self.buttonsLayout.setAlignment(Qt.AlignTop)

        self.scane = QPushButton(self.buttons)
        self.scane.setMinimumSize(QSize(16777215, 50))
        self.scane.setObjectName("scane")
        self.scane.setText("SCANE")
        self.scane.setCursor(QCursor(Qt.PointingHandCursor))
        self.scane.clicked.connect(self.scaneUpdateProgressBar)

        self.addDir = QPushButton(self.buttons)
        self.addDir.setMinimumSize(QSize(16777215, 50))
        self.addDir.setObjectName("addDir")
        self.addDir.setText("ADD DIR")
        self.addDir.setCursor(QCursor(Qt.PointingHandCursor))
        self.addDir.clicked.connect(self.addDirUpdateList)

        self.delDir = QPushButton(self.buttons)
        self.delDir.setMinimumSize(QSize(16777215, 50))
        self.delDir.setObjectName("delDir")
        self.delDir.setText("DEL DIR")
        self.delDir.setCursor(QCursor(Qt.PointingHandCursor))
        self.delDir.clicked.connect(self.delDirUpdateList)

    def setProgressBars(self):
        self.vpbar = QProgressBar(self.buttons)
        self.vpbar.setMinimumSize(QSize(100, 10))
        self.vpbar.setObjectName("values_progressbar")

        self.dpbar = QProgressBar(self.buttons)
        self.dpbar.setMinimumSize(QSize(100, 10))
        self.dpbar.setObjectName("dirs_progressbar")

    def setList(self):
        self.list = QListWidget(self.dirsControleFrame)

        self.list.setAutoFillBackground(True)
        self.list.setViewMode(QListView.ListMode)
        self.list.setCursor(QCursor(Qt.PointingHandCursor))
        self.list.setSpacing(2)
        self.list.setMaximumSize(QSize(1300, 400))

        self.setListItems()

    def scaneUpdateProgressBar(self):
        if not self.dirs:
            return

        self.dpbar.resetFormat()
        self.vpbar.resetFormat()
        self.scane.setEnabled(False)
        self.thread = scaneThread(self.dirs)
        self.thread._currentValueSignal.connect(self.updateVProgressBar)
        self.thread._currentDirSignal.connect(self.updateDProgressBar)
        self.thread.start()

    def addDirUpdateList(self):
        documentsPath = path.join(getenv("HOME"), "Documents")
        dirPath = QFileDialog.getExistingDirectory(self, "Choose A Directory",
                                                   documentsPath)
        if not dirPath:
            return

        conn = connect(DB_PATH)
        Dir = Dirent(dirPath)
        commit_dir(conn, Dir)
        conn.close()
        self.updateList()

    def delDirUpdateList(self):
        if not dirPath:
            return

        conn = connect(DB_PATH)
        Dir = Dirent(dirPath)
        commit_dir(conn, Dir)
        conn.close()
        self.updateList()

    def setListItems(self):
        conn = connect(DB_PATH)
        dirs = fetch_dirs(conn)
        conn.close()

        for _dir in dirs:
            self.dirs.append(_dir.path)
            self.list.addItem(_dir.path)

    def updateList(self):
        self.list.clear()
        self.setListItems()

    def updateVProgressBar(self, msg):
        self.vpbar.setValue(int(msg))
        if self.vpbar.value() >= 99:
            self.vpbar.setValue(0)
            self.vpbar.setFormat("Done")

    def updateDProgressBar(self, msg):
        self.dpbar.setValue(int(msg))
        if self.dpbar.value() >= 99:
            self.dpbar.setValue(0)
            self.scane.setEnabled(True)
            self.dpbar.setFormat("Done")


class SettingsPage(QWidget):

    def __init__(self, QParent, parent=None):
        super().__init__(QParent)
        self.setObjectName("pageSettings")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("settings_layout")

        with open("epookman/ui/QSS/settingsPage.qss", "r") as f:
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
        self.label.setObjectName("title")
        self.label.setText("SETTINGS")

    def setContent(self, content):
        self.content = content

    def setLayoutes(self):
        self.topbarLayout.addWidget(self.label)
        self.layout.addWidget(self.topbar)
        self.layout.addWidget(self.content)
