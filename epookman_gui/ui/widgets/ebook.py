#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.

import subprocess
from os import getenv, path

from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QCursor, QIcon, QPixmap)
from PyQt5.QtWidgets import (QFrame, QListWidgetItem, QMenu)

from epookman_gui.api.db import DB_PATH, commit_ebook, connect
from epookman_gui.api.ebook import (STATUS_HAVE_NOT_READ, STATUS_HAVE_READ,
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


class EbookItem(QListWidgetItem):

    def __init__(self, QParent, ebook, parent=None):
        super().__init__(QParent)
        self.parent = parent
        self.ebook = ebook

        self.setText(ebook.name)
        self.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.setToolTip(ebook.metadata)
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

    def markFav(self):
        self.ebook.toggle_fav()
        self.commit()

    def markDone(self):
        self.ebook.set_status(STATUS_HAVE_READ)
        self.commit()

    def markToRead(self):
        self.ebook.set_status(STATUS_HAVE_NOT_READ)
        self.commit()

    def markReading(self):
        self.ebook.set_status(STATUS_READING)
        self.commit()

    def commit(self):
        conn = connect(DB_PATH)
        commit_ebook(conn, self.ebook)
        conn.commit()
        conn.close()
