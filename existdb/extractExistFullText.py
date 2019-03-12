#!/usr/bin/env python
import xml.etree.ElementTree as ET


class ExtractExistFullText:

    def __init__(self):
        pass

    def extract_text(self, filename):

        full_text_file = open(filename, 'r')
        id = filename[9:-4]

        tree = ET.parse(full_text_file)


        root = tree.getroot()
        pages = root.findall('./pages/page/fullText/body')


        holder = ''
        for page in pages:

            holder += ' '.join(page.itertext())

        return holder
