
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


class CustomFormatField:

    format_fields = {}

    def __init__(self):
        pass

    @staticmethod
    def append_to_dimension(dimen):
        if len(dimen) > 0:
            return dimen + ' x '

    def add_format(self, key, value):
        # type: (str, str) -> None
        """
        Adds a candidate format field to the dictionary

        :param key: the dimension or unit
        :param value: the text
        """
        self.format_fields[key] = value

    def add_custom_format_element(self, tree):
        # type: (Element) -> None
        """
        Adds a format.extend field to the dublin core tree if the field conditions are met.

        :param tree: The parent Dublin Core element tree.
        """
        text = ''
        fields = len(self.format_fields)
        if 'height' in self.format_fields:
            text += self.format_fields['height']
            if fields - 1 > 1:
                text += ' x '
                fields -= 1
        if 'width' in self.format_fields:
            text += self.format_fields['width']
            if fields - 1 > 1:
                text += ' x '
                fields -= 1
        if 'depth' in self.format_fields:
            text += self.format_fields['depth']
            if fields - 1 > 1:
                text += ' x '
                fields -= 1
        if 'units' in self.format_fields:
            text += ' ' + self.format_fields['units']

        if len(text) > 0:
            sub_element = ET.SubElement(tree, 'dcvalue')
            sub_element.set('element', 'format')
            sub_element.set('qualifier', 'extent')
            sub_element.text = text
