#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""Epookman class and functions"""

# TODOO: Configuration file
# TODO: Threads, for scane
# TODO: tests
# TODO: command line arguments
# TODOOO: Signal handling
# FIXMEE: ebooks from sub dirs are deleted when deleting main dirs

import curses
import os
import re
from time import sleep

import magic

from epookman.api.db import *
from epookman.api.dirent import Dirent, check_path
from epookman.api.ebook import Ebook
from epookman.api.mime import Mime
from epookman.core.config import Config

class Epookman(object):
    """Epookman main class"""

    def __init__(self, stdscreen):
        self.db_name = "epookman.db"
        self.db_path = os.path.join(os.getenv("HOME"), self.db_name)

        self.db_init(self.db_path)
        self.db_fetch(self.conn)

        self.ebooks_files_init()

        self.main_menu = None
        self.screen = stdscreen

        self.menu_window_init()
        self.statusbar = StatusBar(stdscreen)

        self.ebook_reader = Config.ebook_reader

    def __del__(self):
        self.close_connection()

    def addir(self, Dir):
        if isinstance(Dir, Dirent) and Dir not in self.dirs:
            self.dirs.append(Dir)
            return True

        else:
            return False

    def addir_commit(self, conn, Dir):
        if self.addir(Dir):
            commit_dirs(conn, self.dirs)

    def addirs_commit(self, conn, uris):
        if not isinstance(uris, list) and not isinstance(uris, tuple):
            return

        else:
            for uri in uris:
                Dir = Dirent(uri)
                self.addir_commit(conn, Dir)

    def close_connection(self):
        if self.conn:
            self.conn.close()

        self.conn = None

    def ebooks_files_init(self):
        self.ebooks_files = [
            os.path.join(ebook.folder, ebook.name) for ebook in self.ebooks
        ]

    def del_dir(self, conn, path):
        del_dir(conn, path)
        del_ebooks(conn, directory=path)

        for Dir in self.dirs:
            if Dir.path == path:
                self.dirs.remove(Dir)

    def del_dir_refetch(self, conn, path):
        self.del_dir(conn, path)
        self.dirs = fetch_dirs(conn)
        self.ebooks = fetch_ebooks(conn)
        self.ebooks_files_init()

        self.statusbar.print("Directory has been deleted",
                             curses.color_pair(4))
        # Delay to make the message visable
        sleep(.5)
        self.kill_rerun_main_menu()

    def db_init(self, db_path):
        self.conn = connect(db_path)
        self.cur = self.conn.cursor()

        create_tables(self.conn)

    def db_fetch(self, conn):

        self.dirs = fetch_dirs(conn)

        self.ebooks = fetch_ebooks(conn)

    def input_add_dir(self):
        string = self.statusbar.input("Directory path: ")
        if not string:
            return
        if string.startswith("~"):
            string = string.replace("~", os.getenv("HOME"))
        string = os.path.realpath(string)
        if not check_path(string):
            self.statusbar.print("Not a valid path", curses.color_pair(5))
            return

        Dir = Dirent(string)
        self.addir_commit(self.conn, Dir)
        self.statusbar.print("Directory has been added to database")

    def kill_rerun_main_menu(self):
        self.make_menus()
        self.main_menu.kill()
        self.main_menu.init_window()
        if self.main_menu.display() == -1:
            self.exit(0)

    def menu_window_init(self):
        y_val = self.screen.getmaxyx()[0]
        self.menu_window = self.screen.subwin(y_val - Config.padding - 1, 0, 0,
                                              0)

    def make_menus(self):

        # reading menu
        reading_menu_items = [{
            "string": ebook.name,
            "enter_action": self.open_ebook,
            "args": (ebook, ),
            "type": "ebook",
            "take_action": self.take_action,
        } for ebook in fetch_ebooks(self.conn,
                                    where=f"status={Ebook.STATUS_READING}")]
        reading_menu = Menu("reading", reading_menu_items, self.menu_window)

        # have read menu
        have_read_menu_items = [{
            "string": ebook.name,
            "enter_action": self.open_ebook,
            "args": (ebook, ),
            "type": "ebook",
            "take_action": self.take_action
        } for ebook in fetch_ebooks(self.conn,
                                    where=f"status={Ebook.STATUS_HAVE_READ}")]
        have_read_menu = Menu("have_read", have_read_menu_items,
                              self.menu_window)

        # haven't read menu
        havent_read_menu_items = [{
            "string": ebook.name,
            "enter_action": self.open_ebook,
            "args": (ebook, ),
            "type": "ebook",
            "take_action": self.take_action
        } for ebook in fetch_ebooks(
            self.conn, where=f"status={Ebook.STATUS_HAVE_NOT_READ}")]
        havent_read_menu = Menu("havent_read", havent_read_menu_items,
                                self.menu_window)

        # all menu
        all_menu_items = [{
            "string": ebook.name,
            "enter_action": self.open_ebook,
            "args": (ebook, ),
            "type": "ebook",
            "take_action": self.take_action
        } for ebook in fetch_ebooks(self.conn)]
        all_menu = Menu("all", all_menu_items, self.menu_window)

        # folders menu
        folders_menu_items = []
        self.dirs = fetch_dirs(self.conn)
        for Dir in self.dirs:
            dir_ebooks = [
                ebook
                for ebook in fetch_ebooks(self.conn,
                                          where=f"folder like \'{Dir.path}%\'")
            ]
            dir_menu_items = [{
                "string": ebook.name,
                "enter_action": self.open_ebook,
                "args": (ebook, ),
                "type": "ebook",
                "take_action": self.take_action
            } for ebook in dir_ebooks]
            dir_menu = Menu(Dir.path, dir_menu_items, self.menu_window)
            folders_menu_items.append({
                "string": Dir.path,
                "enter_action": dir_menu.display,
                "type": "dir",
                "take_action": self.take_action
            })

        folders_menu = Menu("folders", folders_menu_items, self.menu_window)

        # categories menu
        categories_menu_items = []
        categories_list = fetch_ebooks(self.conn, key="category")
        for cat in categories_list:
            cat_ebooks = [
                ebook for ebook in fetch_ebooks(self.conn,
                                                where="category=\'%s\'" % cat)
            ]
            cat_menu_items = [{
                "string": ebook.name,
                "enter_action": self.open_ebook,
                "args": (ebook, ),
                "type": "ebook",
                "take_action": self.take_action
            } for ebook in cat_ebooks]
            cat_menu = Menu(cat, cat_menu_items, self.menu_window)
            categories_menu_items.append({
                "string": cat,
                "enter_action": cat_menu.display,
                "type": "cat",
                "take_action": self.take_action
            })

        categories_menu = Menu("categories", categories_menu_items,
                               self.menu_window)

        # favorites menu
        favorites_menu_items = [{
            "string": ebook.name,
            "enter_action": self.open_ebook,
            "args": (ebook, ),
            "type": "ebook",
            "take_action": self.take_action
        } for ebook in fetch_ebooks(self.conn, where="fav=1")]
        favorites_menu = Menu("favorites", favorites_menu_items,
                              self.menu_window)

        main_menu_items = (
            {
                "string": "Reading",
                "enter_action": reading_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "Folders",
                "enter_action": folders_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "Favorites",
                "enter_action": favorites_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "Categories",
                "enter_action": categories_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "Have read",
                "enter_action": have_read_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "Haven't read",
                "enter_action": havent_read_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
            {
                "string": "All",
                "enter_action": all_menu.display,
                "type": "menu",
                "take_action": self.take_action
            },
        )

        self.main_menu = Menu("main", main_menu_items, self.menu_window)

    def open_ebook(self, ebook):
        uri = ebook.get_path()

        cmd = "%s \"%s\" > /dev/null 2>&1" % (self.ebook_reader, uri)
        if os.system(cmd) < 0:
            msg = "Couldn't open %s" % uri

        self.change_ebook_info(ebook=ebook, status=Ebook.STATUS_READING)
        self.kill_rerun_main_menu()

    def change_ebook_info(self,
                          status=None,
                          fav=None,
                          category=None,
                          ebook=None,
                          name=None):
        if name:
            for i in self.ebooks:
                if i.name == name:
                    ebook = i

        elif not ebook:
            return

        if fav:
            ebook.toggle_fav()

        elif status != None:
            ebook.set_status(status)

        elif category:
            ebook.set_category(category)

        for index, i in enumerate(self.ebooks):
            if i.name == ebook.name:
                self.ebooks[index] = ebook

        commit_ebook(self.conn, ebook)
        status = ebook.get_status_string(status)

    def scane(self):
        mime = Mime()
        self.ebooks_files_init()

        for Dir in self.dirs:
            Dir.getfiles()
            for file in Dir.files:
                mime_type = mime.mime_type(file)
                if mime_type:
                    if mime.is_ebook(
                            mime_type) and file not in self.ebooks_files:
                        ebook = Ebook()
                        ebook.set_path(file)
                        ebook.set_type(mime_type)
                        self.ebooks.append(ebook)

    def scane_commit(self, conn):
        self.statusbar.print("Scanning for ebooks...")
        self.scane()

        update_db(conn, self.dirs, self.ebooks)
        self.statusbar.print("Saving changes to database...")

        self.statusbar.print("Done.", curses.color_pair(4))

    def take_action(self, key, args=None, value=None):
        if key == "scane":
            self.scane_commit(self.conn)

        elif key == "toggle_mark":
            args = args[0]
            self.change_ebook_info(ebook=args, status=value)
            value = Ebook.get_status_string(value)
            self.statusbar.print("Ebook marked as %s" % value,
                                 curses.color_pair(4))

        elif key == "toggle_fav":
            args = args[0]
            self.change_ebook_info(ebook=args, fav=True)
            self.statusbar.print("Toggled ebook favorite",
                                 curses.color_pair(4))

        elif key == "add_category":
            args = args[0]
            self.change_ebook_info(ebook=args, category=value)
            self.statusbar.print("Ebook add to category %s" % value,
                                 curses.color_pair(4))

        elif key == "add_dir":
            self.input_add_dir()

        elif key == "del_dir":
            args = args[0]
            if self.statusbar.confirm(
                    "Are you sure want to delete this directory? [y, n]: ",
                    curses.color_pair(5)):
                self.del_dir_refetch(self.conn, args)

        elif key == "print_status":
            args = args[0]
            self.statusbar.print(args)

        self.kill_rerun_main_menu()
        self.statusbar.print("Press ? to show help.")

    def main(self):
        self.make_menus()
        self.statusbar.print("Press ? to show help.")
        if self.main_menu.display() == -1:
            self.exit(0)

    def exit(self, status):
        exit(status)
