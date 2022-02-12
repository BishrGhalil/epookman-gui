#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of epookman_gui, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""Epookman theme generator"""

import re
from json import loads


def themer(theme) -> str:
    colors = {}
    with open(f"epookman_gui/ui/themes/{theme}.json", "r") as theme_file:
        colors = loads(theme_file.read())

    style = ""
    with open("epookman_gui/ui/themes/style.qss", "r") as style_file:
        style = style_file.read()
        for color in colors:
            style = re.sub(color, colors[color], style)

    return style
