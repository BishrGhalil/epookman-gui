#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui.
# License: MIT, see the file "LICENCS" for details.
"""Epookman theme generator"""

import re
from json import loads
from os import (getenv, path)


def themer(theme) -> str:
    colors = {}
    home = path.expanduser('~')
    themes_path = path.join(home, ".config/epookman-gui/themes")
    try:
        if not path.lexists(themes_path):
            themes_path = "epookman_gui/ui/themes"
    except:
        return ""

    with open(f"{themes_path}/{theme}.json", "r") as theme_file:
        colors = loads(theme_file.read())

    style = ""
    with open(f"{themes_path}/style.qss", "r") as style_file:
        style = style_file.read()
        for color in colors:
            style = re.sub(color, colors[color], style)

    return style
