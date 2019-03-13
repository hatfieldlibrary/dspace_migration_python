#!/usr/bin/env python
import xml.etree.ElementTree as ET


class ExtractExistFullText:

    def __init__(self):
        pass

    def extract_text(self, filename):

        full_text_file = open(filename, 'r')

        tree = ET.parse(full_text_file)

        root = tree.getroot()
        pages = root.findall('./pages/page/fullText/body')

        # NOTE: This simple extraction includes word segments when hyphenation occurs.
        # For example: "per personal sonal"
        # This can probably be fixed...
        holder = ''
        for page in pages:
            holder += ' '.join(page.itertext())

        return holder
