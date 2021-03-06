#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""Epookman database handling functions"""

import sqlite3

from epookman_gui.api.dirent import Dirent
from epookman_gui.api.ebook import Ebook
from os import getenv


# Connect and Disconnect functions
def connect(db_path):
    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn):
    conn.close()


# Create tables functions


def create_dirs_table(conn):
    cur = conn.cursor()
    cur.execute(
            "CREATE TABLE IF NOT EXISTS DIRS(" \
            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
            "PATH           TEXT NOT NULL," \
            "RECURS         INT NOT NULL);"
    )

    conn.commit()


def create_ebooks_table(conn):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS EBOOKS(" \
        "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
        "NAME           TEXT    NOT NULL," \
        "FOLDER         TEXT    NOT NULL," \
        "PARENT_FOLDER  TEXT    NOT NULL," \
        "TYPE           INT    NOT NULL," \
        "CATEGORY       TEXT," \
        "STATUS         INT," \
        "FAV            INT);")

    conn.commit()


def create_ebooks_index(conn, index_key):
    cur = conn.cursor()
    cur.execute(
        "CREATE INDEX IF NOT EXISTS " \
        f"idx_{index_key.lower()} ON EBOOKS ({index_key.upper()});"
    )

    conn.commit()


def create_ebooks_indexes(conn):
    indexes = ["fav", "category", "status", "parent_folder"]
    for index_key in indexes:
        create_ebooks_index(conn, index_key)


def create_tables(conn):
    create_dirs_table(conn)
    create_ebooks_table(conn)
    create_ebooks_indexes(conn)


# Insert and update functions


def commit_dirs(conn, dirs):
    for Dir in dirs:
        commit_dir(conn, Dir)


def commit_dir(conn, Dir):
    cur = conn.cursor()
    data = (Dir.path, Dir.path, Dir.recurs)
    cur.execute(
        "INSERT OR REPLACE \
        INTO DIRS (ID, PATH, RECURS) \
        VALUES \
        ((SELECT ID FROM DIRS WHERE PATH = ?), ?, ?);", data)

    conn.commit()


def commit_ebooks(conn, ebooks):
    for ebook in ebooks:
        commit_ebook(conn, ebook)
        conn.commit()


def commit_ebook(conn, ebook):
    cur = conn.cursor()
    data = (ebook.name, ebook.name, ebook.folder, ebook.parent_folder,
            ebook.type, ebook.category, ebook.status, ebook.fav)
    cur.execute(
        "INSERT OR REPLACE "\
        "INTO EBOOKS (ID, NAME, FOLDER, PARENT_FOLDER, " \
        "TYPE, CATEGORY, STATUS, FAV) " \
        "VALUES ((SELECT ID FROM EBOOKS WHERE NAME = ?), ?, ?, ?, ?, ?, ?, ?);",
        data)


def del_ebooks(conn, directory=None, name=None, category=None):
    cur = conn.cursor()
    if directory:
        cur.execute(f"DELETE FROM EBOOKS WHERE PARENT_FOLDER = '{directory}';")
    elif name:
        cur.execute(f"DELETE FROM EBOOKS WHERE NAME = '{name}';")
    elif category:
        cur.execute(f"DELETE FROM EBOOKS WHERE CATEGORY = '{category}';")

    conn.commit()


# Fetching functions


def fetch_ebooks(conn, key="*", where=None, sort_clause=None):
    if not sort_clause:
        sort_clause = "ORDER BY NAME, FAV DESC"

    if not where:
        query = f"SELECT DISTINCT {key} FROM EBOOKS {sort_clause};"

    else:
        query = f"SELECT DISTINCT {key} FROM EBOOKS WHERE {where} {sort_clause};"

    cur = conn.cursor()
    res = cur.execute(query)
    ebooks = list()

    if not res:
        return ebooks

    for row in res:
        if len(row) == 1:
            ebooks.append(row[0])
        else:
            ebook = Ebook(
                name=row[1],
                folder=row[2],
            )
            ebook.set_parent_folder(row[3])
            ebook.set_type(row[4])
            ebook.set_category(row[5])
            ebook.set_status(row[6])
            ebook.set_fav(row[7])
            ebooks.append(ebook)

    return ebooks


def fetch_dirs(conn):
    cur = conn.cursor()
    res = cur.execute("SELECT DISTINCT * FROM DIRS ORDER BY PATH;")
    dirs = list()

    if not res:
        return dirs

    for row in res:
        Dir = Dirent()
        Dir.set_values(row[1], row[2])
        dirs.append(Dir)

    return dirs
