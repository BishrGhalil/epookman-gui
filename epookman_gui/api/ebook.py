#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""Ebook functions and consts"""

import os
from epub_meta import get_epub_metadata
from PyPDF2 import PdfFileReader
from re import search

EBOOK_TYPE_PDF = 0
EBOOK_TYPE_EPUB = 1
EBOOK_TYPE_MOBI = 2
EBOOK_TYPE_XPS = 3
EBOOK_TYPE_CBR = 4
EBOOK_TYPE_CBZ = 5

STATUS_HAVE_NOT_READ = 0
STATUS_READING = 1
STATUS_HAVE_READ = 2


class Ebook():
    STATUS_HAVE_NOT_READ = 0
    STATUS_READING = 1
    STATUS_HAVE_READ = 2

    def __init__(self,
                 _id=0,
                 folder="",
                 name="",
                 category=None,
                 status=0,
                 fav=0,
                 ebook_type=None,
                 metadata=None):

        self.ebook_types = {
            "pdf": EBOOK_TYPE_PDF,
            "epub": EBOOK_TYPE_EPUB,
            "mobi": EBOOK_TYPE_MOBI,
            "xps": EBOOK_TYPE_XPS,
            "cbr": EBOOK_TYPE_CBR,
            "cbz": EBOOK_TYPE_CBZ
        }

        self.name = name
        self.id = _id
        self.folder = folder
        self.category = category
        self.status = status
        self.fav = fav
        self.path = self.get_path()
        self.set_type(ebook_type)
        self.metadata = metadata

    def set_path(self, path):
        self.path = path
        self.folder = os.path.dirname(path)
        self.name = os.path.basename(path)

    def set_status(self, status):
        self.status = status

    def set_category(self, category):
        self.category = category

    def set_type(self, _type):
        if type(_type) == str:
            for ebook_type in self.ebook_types.keys():
                if search(ebook_type, _type):
                    self.type = self.ebook_types.get(ebook_type)
                    return
        else:
            self.type = _type if _type in self.ebook_types.values() else None

    def set_fav(self, fav):
        self.fav = fav

    def set_name(self, name):
        self.name = name

    def set_folder(self, folder):
        self.folder = folder

    def set_parent_folder(self, parent_folder):
        self.parent_folder = parent_folder

    def set_metadata(self, metadata):
        self.metadata = metadata

    def toggle_fav(self):
        self.fav = not self.fav

    def get_path(self):
        uri = os.path.join(self.folder, self.name)
        return uri

    @classmethod
    def get_status_string(cls, status):
        if status == cls.STATUS_HAVE_NOT_READ:
            return "Have not read"
        elif status == cls.STATUS_HAVE_READ:
            return "Have read"
        elif status == cls.STATUS_READING:
            return "Reading"

    def get_type_string(self):
        for ebook_type in self.ebook_types.keys():
            if self.type == self.ebook_types.get(ebook_type):
                return ebook_type

    def get_fav_string(self):
        if self.fav:
            return "True"
        else:
            return "False"

    def get_data(self):
        data = {
            "name": self.name,
            "type": self.get_type_string(),
            "category": self.category,
        }

        return data

    def get_meta_data(self):
        data = dict()

        path = self.get_path()
        size = os.stat(path)
        size = "%.2f" % (size.st_size / (1024**2))
        data["File Size"] = size + "M"
        try:
            if self.type == self.ebook_types.get("pdf"):
                with open(path, "rb") as file:
                    pdfreader = PdfFileReader(file)
                    if not data.get("Encrypt"):
                        data["Pages"] = pdfreader.numPages
                        info = pdfreader.documentInfo
                        data["Creators"] = info.get('/Creator')

            elif self.type == self.ebook_types.get("epub"):
                tmp_data = get_epub_metadata(path,
                                             read_cover_image=False,
                                             read_toc=False)
                data["Creation"] = tmp_data.publication_date
        except Exception as e:
            data = dict()

        return data

    def get_meta_data_string(self):
        data = self.get_data()
        metadata = self.get_meta_data()
        data.update(metadata)
        string = ""
        keys = data.keys()
        keys_len = len(keys)

        for index, key in enumerate(keys):
            string += "%-20s\t%s" % (key, data.get(key))
            if index < keys_len - 1:
                string += "\n"

        return string

    def update_meta_data_string(self):
        self.metadata = self.get_meta_data_string()
