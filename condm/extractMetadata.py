#!/usr/bin/env python

import xml.etree.ElementTree as ET
from extractPageData import ExtractPageData
from fields import Fields
from fieldMaps import FieldMaps


class ExtractMetadata:

    def __init__(self):
        self.extract_page = ExtractPageData()

    @staticmethod
    def isSingleItem(record):
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
    def processIterableMap(parent_element, elements, element_map):
        """
        Use this function to process any iterable list of etree elements.
        (Provided that the element requires no special logic.) This method
        adds the new sub-elements to the parent element.
        :param parent_element: the parent etree Element to which sub-elements will be added.
        :param elements: the list of etree elements to read.
        :param element_map: the dictionary for cdm to dspace mapping.
        """
        cdm_dc = Fields.cdm_dc_field
        if elements is not None:
                for element in elements:
                    if element.text is not None:
                        # It makes no sense add unmapped fields to dspace dublin core.
                        # These need to be exported differently from cdm if we need them.
                        # The 'unmapped' key has been included (temporarily?) in the cdm field dictionary
                        # and is used in the hack that captures a subset of EADID local fields.
                        # See extractLocalMetadata() below.
                        if element.tag != cdm_dc['unmapped']:
                            dspace_element = element_map[element.tag]
                            sub_element = ET.SubElement(parent_element, 'dcvalue')
                            sub_element.set('element', dspace_element['element'])
                            if dspace_element['qualifier'] is not None:
                                sub_element.set('qualifier', dspace_element['qualifier'])
                            sub_element.text = element.text

    def extractLocalMetadata(self, record):
        """
        This method extracts the metadata to add metadata_local.xml in the saf directory.
        Data fields are mapped to the local metadata registry configured for our dspace instance.
        :param record: etree Element representing the contentdm record.
        :return: a new etree Element representing data that will be written to metadata_local.xml.
        """
        cdm_dc = Fields.cdm_dc_field
        cdm_structure = Fields.cdm_structural_elements
        dspace_local = Fields.dspace_local_field
        dspace_local_map = FieldMaps.local_field_map

        metadata_local = ET.Element('metadata_local')
        metadata_local.set('schema', 'local')

        cdmfullResolution = record.iterfind(cdm_structure['preservation_location'])
        # This should probably be considered a hack.
        cdmunmapped = record.iterfind(cdm_dc['unmapped'])

        # TODO: the eadid needs to be mapped to a unique field. For now, use string match so some eadid fields will
        #  appear in dspace.
        for element in cdmunmapped:
            if element.text is not None:
                if element.text.find('WUA') != -1:
                    relation_references = ET.SubElement(metadata_local, 'dcvalue')
                    relation_references.set('element', dspace_local['eadid'])
                    relation_references.text = element.text

        self.processIterableMap(metadata_local, cdmfullResolution, dspace_local_map)
        self.extract_page.addPageAdminData(metadata_local, record)

        return metadata_local

    def extractMetadata(self, record):
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.
        :param record: the etree Element for the contentdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        cdm_dc = Fields.cdm_dc_field
        dspace_dc = Fields.dspace_dc_field
        dc_field_map = FieldMaps.dc_field_map

        dublin_core = ET.Element('dublin_core')
        dublin_core.set('schema', 'dc')

        # Because this uses sorted keys, the field order is alphabetical.
        cdm_keys = sorted(cdm_dc.keys())
        for key in cdm_keys:
            if key in cdm_keys:
                elements = record.iterfind(cdm_dc[key])
                if key == cdm_dc['format']:
                    if not self.isSingleItem(record):
                         # Sets the format for compound objects.
                        cpdformat = ET.SubElement(dublin_core, 'dcvalue')
                        cpdformat.set('element', dspace_dc['format'])
                        cpdformat.text = 'Compound'
                    else:
                        self.processIterableMap(dublin_core, elements, dc_field_map)
                else:
                    self.processIterableMap(dublin_core, elements, dc_field_map)

        return dublin_core
