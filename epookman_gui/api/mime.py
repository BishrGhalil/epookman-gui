#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""Check file mime type"""

from re import search

import magic

MIME_TYPE_EBOOK_PDF = 0
MIME_TYPE_EBOOK_EPUB = 1
MIME_TYPE_EBOOK_MOBI = 2
MIME_TYPE_EBOOK_XPS = 3
MIME_TYPE_EBOOK_CBR = 4
MIME_TYPE_EBOOK_CBZ = 5


class Mime():

    def __init__(self):
        self.mime = magic.open(magic.MAGIC_MIME)
        self.mime.load()
        self.re_ebooks_types = {
            "pdf": MIME_TYPE_EBOOK_PDF,
            "epub": MIME_TYPE_EBOOK_EPUB,
            "mobi": MIME_TYPE_EBOOK_MOBI,
            "xps": MIME_TYPE_EBOOK_XPS,
            "cbr": MIME_TYPE_EBOOK_CBR,
            "cbz": MIME_TYPE_EBOOK_CBZ
        }

    def mime_type(self, file):
        mime_t = self.mime.file(file)
        for ebook_type in self.re_ebooks_types.keys():
            if search(ebook_type, mime_t):
                return self.re_ebooks_types.get(ebook_type)
        return None

    def is_ebook(self, mime_type):
        if MIME_TYPE_EBOOK_PDF <= mime_type <= MIME_TYPE_EBOOK_CBZ:
            return True

        else:
            return False

    def is_ebook_from_path(self, file):
        for ebook_type in self.re_ebooks_types.keys():
            if search(ebook_type, file):
                return self.re_ebooks_types.get(ebook_type)

        return False
