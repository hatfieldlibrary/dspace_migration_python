#!/usr/bin/env python

import xml.etree.ElementTree as ET
from collections import Iterable
from xml.etree.ElementTree import Element

from extractExistFullText import ExtractExistFullText
from existDbFields import ExistDbFields
from existDbFieldMaps import ExistDbFieldMaps
from existDbFieldDefaults import DefaultFieldValueMap


class ExtractMetadata:
    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    def __init__(self):
        self.extract_page = ExtractExistFullText()

    @staticmethod
    def add_sub_element(parent, element_map, value):
        # type: (Element, dict, str) -> None
        """
        Use this method to add a new element to the saf xml.
        :param parent: saf xml
        :param element_map: dspace mapping for a single element
        :param value: the text value
        """
        sub_element = ET.SubElement(parent, 'dcvalue')
        sub_element.set('element', element_map['element'])
        if element_map['qualifier'] is not None:
            sub_element.set('qualifier', element_map['qualifier'])
        sub_element.text = value

    def __process_iterable_map(self, parent_element, elements, element_map):
        # type: (Element, Iterable, dict) -> None
        """
        Use this function to process a list of etree elements using
        an existdb to DSpace field map.

        :param parent_element: the parent etree Element to which sub-elements will be added.
        :param elements: the list of etree elements to read.
        :param element_map: the dictionary for cdm to dspace mapping.
        """
        if elements is not None:

            citation = ''

            for element in elements:
                if element.text is not None:
                    # first, remove the namespace
                    if element.tag.startswith("{"):
                        element.tag = element.tag.split('}', 1)[1]
                    if element.tag == 'detail':
                        # accumulate citation information
                        citation_type = element.attrib['type']
                        if citation_type == 'volume':
                            citation += 'volume ' + element[0].text
                        if citation_type == 'issue':
                            citation += ' issue ' + element[0].text
                        if citation_type == 'edition':
                            citation += ' edition ' + element[0].text
                    else:
                        # add a new sub-element.
                        self.add_sub_element(parent_element, element_map[element.tag], element.text)

            if len(citation) > 0:
                # add identifier.citation sub-element.
                self.add_sub_element(parent_element, element_map['detail'], citation)

    @staticmethod
    def is_single_item(record):
        # type: (Element) -> bool
        """
        Tests for compound object. If a page sub-element does not exist, this is a
        single item.

        :param record: the etree element for the contentdm record.
        :return: boolean true if a single item and false if compound object.
        """
        structure = record.find('structure')
        page = structure.find('.//page')

        return page is None

    @staticmethod
    def add_default_metadata(dublin_core):
        # type: (Element) -> None
        """
        If the record does not contain a field that has a
        default value, add that default value to the record.
        :param dublin_core: the current saf xml
        :return: updated saf xml
        """
        defaults = DefaultFieldValueMap.default_values
        for element in defaults.keys():
            qry = ".//*[@element='%s']"%element
            e = dublin_core.findall(qry)
            if len(e) == 0:
                sub_element = ET.SubElement(dublin_core, 'dcvalue')
                sub_element.set('element', element)
                sub_element.text = defaults[element].get('value')

    def get_mets_element(self, field, section):
        # type: (Object, Element) -> Element
        """
        Extracts element from mets record.

        :param field: the exist field map object for a data resource
        :param record: the etree element for the contentdm record.
        :return: boolean true if a single item and false if compound object.
        """
        element = field.get('element')
        attr = field.get('attr')
        attr_val = field.get('attr_val')

        if attr is not None and attr_val is not None:
                qry = ".//%s[@%s='%s']" % (element, attr, attr_val[0])
                return section.findall(qry, self.ns)
        else:
            qry = ".//%s"%element
            return section.findall(qry, self.ns)

    def extract_local_metadata(self, record):
        # type: (Element) -> Element
        """
        NOTE: Currently not using a local field for mets data.

        This method extracts the metadata to add metadata_local.xml in the saf directory.
        Data fields are mapped to the local metadata registry configured for our dspace instance.

        :param record: etree Element representing the contentdm record.
        :return: a new etree Element representing data that will be written to metadata_local.xml.
        """
        metadata_local = ET.Element('dublin_core')
        metadata_local.set('schema', 'local')

        self.extract_page.add_page_admin_data(metadata_local, record)
        return metadata_local

    def extract_metadata(self, record):
        # type: (Element) -> Element
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.

        :param record: the etree Element for the contentdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        # The child elements and attributes to read from the existdb mods element (and also the mets:LABEL).
        exist_elements = ExistDbFields.exist_data_fields
        # The dspace dublin core to write.
        ds_field_map = ExistDbFieldMaps.mods_field_map
        # Structural mets elements and attributes. Used here to retrieve mets:LABEL
        mets_fields = ExistDbFields.mets_structural_elements

        # create the xml element that will be written to saf.
        dublin_core = ET.Element('dublin_core')
        dublin_core.set('schema', 'dc')

        # The item title str.
        item_title_attrib = record.attrib['LABEL']

        # Add the title element
        self.add_sub_element(dublin_core, ds_field_map[mets_fields['label_attr']], item_title_attrib)

        # get the first dmdSec.
        section = record.find('mets:dmdSec', self.ns)

        # Process mods elements in the section.
        mods_keys = sorted(exist_elements.keys())
        for key in mods_keys:
            attr_vals = exist_elements[key]['attr_val']
            # Exist mapping for attribute values is an array.
            if attr_vals is not None:
                for val in attr_vals:
                    if val is not None:
                        # Look up the element by attribute in the mets xml and add to saf xml if elements are found.
                        temp_elements = exist_elements[key]
                        temp_elements['attr_vals'] = val
                        elements = self.get_mets_element(temp_elements, section)
                        if len(elements) > 0:
                            # element found, add to saf xml
                            self.__process_iterable_map(dublin_core, elements, ds_field_map)
            else:
                elements = self.get_mets_element(exist_elements[key], section)
                if elements is not None:
                    # element found, add to saf xml
                    self.__process_iterable_map(dublin_core, elements, ds_field_map)

        # Add any missing values, using the defaults.
        self.add_default_metadata(dublin_core)

        return dublin_core
