#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of epookman, the console ebook manager.
# License: MIT, see the file "LICENCS" for details.
"""PDF thumbnailer"""

from PyPDF2 import PdfFileReader
from os import path


def thumbnailer(file, output=None):
    if not output:
        output = path.dirname(file)
        output = output.removesuffex(".pdf")
        output = output.removesuffex(".epub")
        output += ".jpg"

    reader = PdfFileReader(file)
    page1 = reader.getPage(0)
    with open(output, "w") as file:
        file.write(page1.extractText())
