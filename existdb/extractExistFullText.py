#!/usr/bin/env python
import xml.etree.ElementTree as ET


class ExtractExistFullText:

    def __init__(self):
        pass

    def extract_text(self, filename):
        # type: (str) -> str
        """
        Extracts the full text from the exist-db full text xml file. The result
        returned by this function will be written to the SAF directory as a simple text file.

        :param filename: the path to the full text xml file
        :return: concatenated text from the full text
        """

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
