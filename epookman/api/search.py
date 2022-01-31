#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from epookman.api.db import DB_PATH, commit_ebooks, connect, fetch_ebooks
from epookman.api.ebook import Ebook
from epookman.api.mime import Mime


def scane(dirs):
    ebooks = []
    mime = Mime()
    conn = connect(DB_PATH)
    db_ebooks = fetch_ebooks(conn)
    conn.close()

    ebooks_files = {ebook.path: True for ebook in db_ebooks}

    for Dir in dirs:
        Dir.getfiles()
        for file in Dir.files:
            mime_type = mime.mime_type(file)
            if mime_type:
                if mime.is_ebook(mime_type) and not ebook_file.get(file):
                    ebook = Ebook()
                    ebook.set_path(file)
                    ebook.set_type(mime_type)
                    ebooks.append(ebook)
    return ebooks


def scane_commit(conn, dirs):
    ebooks = scane(dirs)
    commit_ebooks(ebooks)
