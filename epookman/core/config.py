#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""Configurations"""
import curses


class Config():
    padding = 1
    ebook_reader = "zathura"


class Key:
    """functions to check and set keyes"""
    KEY_UP = (ord('k'), curses.KEY_UP)
    KEY_DOWN = (ord('j'), curses.KEY_DOWN)
    KEY_ENTER = (ord('\n'), ord('l'), curses.KEY_RIGHT, curses.KEY_ENTER)
    KEY_LEFT = (ord("h"), curses.KEY_LEFT)
    KEY_MOVE_TOP = (ord('g'), )
    KEY_MOVE_END = (ord('G'), )
    KEY_HELP = (ord('?'), )
    KEY_QUITE = (ord("q"), curses.KEY_EXIT, curses.KEY_CLOSE,
                 curses.KEY_CANCEL)
    KEY_SEARCH = (ord('/'), )
    KEY_ADD = (ord('a'), )
    KEY_FAV = (ord('f'), )
    KEY_HAVE_READ = (ord('r'), )
    KEY_HAVE_NOT_READ = (ord('t'), )
    KEY_SCANE = (ord('u'), )
    KEY_ADD_CATEGORY = (ord('c'), )
    KEY_DEL_DIR = (ord('d'), )
    KEY_SHOW_META_DATA = (ord('s'), )
