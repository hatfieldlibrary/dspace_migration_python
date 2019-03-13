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
        """
        Contructor sets the instance fields for metadata mapping.
        """
        self.extract_page = ExtractExistFullText()
        fieldmap = ExistDbFieldMaps()
        self.ds_field_map = fieldmap.ds_field_map
        self.tag_names = ExistDbFields()

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

            # Use tags without namespace.
            processor_field = self.tag_names.processor_mods_elements

            # Switches between exist and dspace field names.
            #
            # This is here to support a more complex use case, in which we do not want
            # to map all "note" fields to description:statementofresponsibility.
            # Since we may never face this situation, this is a clear violation of the
            # YAGNI principle (https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it)
            #
            # Note that I am still processing the "citation" fields using the dspace map for
            # mods:detail. If there are mods:detail elements that should be handled differently,
            # then we can define a switch for "citations." (BTW, citations include only the volume,
            # issue, edition information and are mapped to dspace identifier:citation. If this should
            # use a different dublin core field, change it in the "ds_field_map".)
            #
            # In sum, "ds_field_map" controls how mods fields are mapped to dublin core. In special cases,
            # a switch can be used to change the mapping.
            switch_tag = self.tag_names.switch_tag

            citation = ''

            for element in elements:
                if element.text is not None:
                    # First, remove the namespace.
                    if element.tag.startswith("{"):
                        element.tag = element.tag.split('}', 1)[1]
                    if element.tag == processor_field['item_details_element']:
                        # Accumulate citation information in details elements, to be added at the
                        # end of this loop.
                        citation_type = element.attrib['type']
                        if citation_type == 'volume':
                            citation += 'volume ' + element[0].text
                        if citation_type == 'issue':
                            citation += ' issue ' + element[0].text
                        if citation_type == 'edition':
                            citation += ' edition ' + element[0].text

                    elif element.tag == processor_field['note_element']:
                        # Note elements contain statement of responsibility (which does map to a dspace dublin
                        # core field)
                        note_type = element.attrib['type']
                        # Slipped in a hard-coded string. This is the value of a type attribute in
                        # the mods:note element.
                        if note_type == 'statement of responsibility':
                            # Because of the switch_tag, the mods:note element will be mapped
                            # to the dublin core description field. See how it's done in existDbFieldMaps.py
                            self.add_sub_element(parent_element,
                                                 element_map[switch_tag['statement_of_responsibility'].get('id')],
                                                 element.text)

                    else:
                        # Just add the new sub-element with no attributes.
                        self.add_sub_element(parent_element, element_map[element.tag], element.text)

            if len(citation) > 0:
                # Add identifier.citation sub-element.
                self.add_sub_element(parent_element, element_map['detail'], citation)

    def __add_default_metadata(self, dublin_core):
        # type: (Element) -> None
        """
        If the record doesn't include a field that has a
        default value, add ta new sub-element to the saf dublin_core.xml.
        :param dublin_core: the current saf xml
        :return: updated saf xml
        """
        # default values to check
        defaults = DefaultFieldValueMap.default_values
        # switch field map
        switch_tag = self.tag_names.switch_tag

        for element in defaults.keys():
            qry = ".//*[@element='%s']"%element
            e = dublin_core.findall(qry)
            if len(e) == 0:
                attr = defaults[element].get('attr')
                if attr is not None:
                    attr_val = defaults[element].get('attr_val')
                    # add more attribute conditions as needed...
                    if attr_val == 'statementofresponsibility':
                        # add new element to parent, using the switch to map description:statementofresponsibility
                        self.add_sub_element(dublin_core,
                                             self.ds_field_map[switch_tag['statement_of_responsibility'].get('id')],
                                             defaults[element].get('value'))
                    else:
                        # add new element to parent sans attributes
                        sub_element = ET.SubElement(dublin_core, 'dcvalue')
                        sub_element.set('element', element)
                        sub_element.text = defaults[element].get('value')

    def __get_mets_element(self, field, section):
        # type: (Object, Element) -> Element
        """
        Extracts and returns sub-element from mets record.

        :param field: the exist field map object for a data resource
        :param section: the etree element for the dmdSec.
        :return: the sub-element
        """
        element = field.get('element')
        attr = field.get('attr')
        attr_val = field.get('attr_val')

        if attr is not None and attr_val is not None:
            # Includes attribute in the query.
            qry = ".//%s[@%s='%s']" % (element, attr, attr_val[0])
            return section.findall(qry, self.ns)
        else:
            qry = ".//%s"%element
            return section.findall(qry, self.ns)

    def extract_metadata(self, record):
        # type: (Element) -> Element
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.

        :param record: the etree Element for the contentdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        # The child elements and attributes to read from the existdb mods element.
        exist_elements = self.tag_names.exist_data_fields

        # Structural mets elements and attributes. Used here to retrieve mets:LABEL
        mets_structural_elements = self.tag_names.mets_structural_elements

        # create the xml element that will be written to saf.
        dublin_core = ET.Element('dublin_core')
        dublin_core.set('schema', 'dc')

        # The item title str.
        item_title_attrib = record.attrib[mets_structural_elements['label_attr']]

        # Add the title element
        self.add_sub_element(dublin_core,
                             self.ds_field_map[mets_structural_elements['label_attr']],
                             item_title_attrib)

        # Get the first dmdSec.
        section = record.find(mets_structural_elements['descriptive_metadata_section'], self.ns)

        # Process mods elements in the section.
        mods_keys = sorted(exist_elements.keys())
        for key in mods_keys:
            attr_vals = exist_elements[key]['attr_val']

            # The exist_elements value for attributes is always an array.
            if attr_vals is not None:
                for val in attr_vals:
                    if val is not None:

                        # Look up the element by attribute in the mets xml and add to
                        # saf xml if elements are found.
                        temp_elements = exist_elements[key]
                        temp_elements['attr_vals'] = val
                        elements = self.__get_mets_element(temp_elements, section)
                        if len(elements) > 0:
                            # Element was found, add to saf xml
                            self.__process_iterable_map(dublin_core,
                                                        elements,
                                                        self.ds_field_map)
            else:
                # No attributes. Just add the element.
                elements = self.__get_mets_element(exist_elements[key], section)
                if elements is not None:
                    # element found, add to saf xml
                    self.__process_iterable_map(dublin_core,
                                                elements,
                                                self.ds_field_map)

        # Add any missing values, using the defaults.
        self.__add_default_metadata(dublin_core)

        return dublin_core
