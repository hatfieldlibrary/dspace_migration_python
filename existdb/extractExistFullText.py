#!/usr/bin/env python
import xml.etree.ElementTree as ET


class ExtractExistFullText:

    def __init__(self):
        pass

    def extract_text(self, filename):

        holder = ''

        try:
            full_text_file = open(filename, 'r')
            tree = ET.parse(full_text_file)
            root = tree.getroot()
            pages = root.findall('./pages/page/fullText/body')
            # NOTE: This simple extraction includes word segments when hyphenation occurs.
            # For example: "per personal sonal"
            # This can probably be fixed...
            for page in pages:
                holder += ' '.join(page.itertext())
        except IOError as err:
            print('IO Error: {0}'.format(err))
            print('WARNING: The full text file does not exist. Return empty text field and continue processing.')

        return holder
