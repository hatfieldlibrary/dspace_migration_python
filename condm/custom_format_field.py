
import xml.etree.ElementTree as ET


class CustomFormatField:

    format_fields = {}

    def __init__(self):
        pass

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
        text = ""
        if len(self.format_fields) == 4:
            text = self.format_fields['width'] + ' x ' \
                   + self.format_fields['height'] \
                   + ' x ' + self.format_fields['depth'] \
                   + ' ' + self.format_fields['units']
        elif len(self.format_fields) == 3:
            text = self.format_fields['width'] + ' x ' \
                   + self.format_fields['height'] + ' ' \
                   + self.format_fields['units']

        if len(self.format_fields) >= 3:
            sub_element = ET.SubElement(tree, 'dcvalue')
            sub_element.set('element', 'format')
            sub_element.set('qualifier', 'extent')
            sub_element.text = text
