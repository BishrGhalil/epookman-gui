#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""Search for ebooks"""

from os import (path, getenv)

from epookman_gui.api.db import (commit_ebooks, connect, fetch_ebooks)
from epookman_gui.api.ebook import Ebook
from epookman_gui.api.mime import Mime
from epookman_gui.api.dirent import Dirent


def scane(dirs):
    ebooks = []
    mime = Mime()
    conn = connect()
    db_ebooks = fetch_ebooks(conn)
    conn.close()

    ebook_files = {ebook.path: True for ebook in db_ebooks}

    for path in dirs:
        Dir = Dirent(uri=path)
        Dir.getfiles()
        for file in Dir.files:
            mime_type = mime.mime_type(file)
            if mime_type != None:
                if mime.is_ebook(mime_type) and not ebook_files.get(file):
                    ebook = Ebook()
                    ebook.set_path(file)
                    ebook.set_type(mime_type)
                    ebook.set_parent_folder(Dir.path)
                    ebook.metadata = ebook.get_meta_data_string()
                    ebooks.append(ebook)
    return ebooks


def scaneOneByOne(dirPath):
    mime = Mime()
    conn = connect()
    db_ebooks = fetch_ebooks(conn)
    conn.close()

    ebook_files = {ebook.path: True for ebook in db_ebooks}

    Dir = Dirent(uri=dirPath)
    Dir.getfiles()
    total = len(Dir.files)
    for i, file in enumerate(Dir.files):
        percent = int(((i) / (total)) * 100)
        mime_type = mime.mime_type(file)
        if mime_type != None:
            if mime.is_ebook(mime_type) and not ebook_files.get(file):
                ebook = Ebook()
                ebook.set_path(file)
                ebook.set_type(mime_type)
                ebook.set_parent_folder(dirPath)
                ebook.set_metadata(ebook.get_meta_data_string())
                yield percent, ebook

        else:
            yield percent, None


def scane_commit(conn, dirs):
    ebooks = scane(dirs)
    commit_ebooks(conn, ebooks)
