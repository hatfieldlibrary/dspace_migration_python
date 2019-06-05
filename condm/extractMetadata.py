#!/usr/bin/env python

import xml.etree.ElementTree as ET
from collections import Iterable
from xml.etree.ElementTree import Element

from extractPageData import ExtractPageData
from fields import Fields
from collection_config import CollectionConfig
from fieldMaps import FieldMaps
from shared.utils import Utils


class ExtractMetadata:

    cdm_dc = Fields.cdm_dc_field

    def __init__(self):
        self.extract_page = ExtractPageData()

    @staticmethod
    def __process_iterable_map(parent_element, elements, element_map):
        # type: (Element, Iterable, dict) -> None
        """
        Use this function to process a list of etree elements using
        a CONTENTdm to DSpace field map. This method adds new sub-elements to the
        parent element (which will later be written to the saf dublin_core.xml).

        :param parent_element: the parent etree Element to which sub-elements will be added.
        :param elements: the list of etree elements to read.
        :param element_map: the dictionary for cdm to dspace mapping.
        """

        if elements is not None:
                for element in elements:
                    if element.text is not None:
                        # It makes no sense add unmapped fields to dspace dublin core.
                        # These need to be exported from cdm differently if we want them.
                        # However, the 'unmapped' key has been included (temporarily?) in the
                        # cdm field dictionary and is used in the hack that captures (some)
                        # EADID local fields. See extractLocalMetadata() below.
                        if element.tag != ExtractMetadata.cdm_dc['unmapped']:
                            # Sometimes CONTENTdm exports encoded text that DSpace doesn't handle.
                            element = Utils.correct_text_encoding(element)
                            dspace_element = element_map[element.tag]
                            sub_element = ET.SubElement(parent_element, 'dcvalue')
                            sub_element.set('element', dspace_element['element'])
                            if dspace_element['qualifier'] is not None:
                                sub_element.set('qualifier', dspace_element['qualifier'])
                            sub_element.text = element.text

    @staticmethod
    def is_single_item(record):
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
    def should_process_compound_as_single(record):
        """
        Checks to see if a compound object record should be treated as a single item. Call
        this function before processing a contentdm compound object record.
        :param record: etree Element representing the contentdm record.
        :return: true if the value in the collection id field is found in the list collection configuration
                array for items that do not need to be loaded as compound objects (e.g. postcards)
        """
        if record.find(ExtractMetadata.cdm_dc['collection_id']) is not None:
            colls = CollectionConfig.collections_to_omit_compound_objects
            els = record.findall(ExtractMetadata.cdm_dc['collection_id'])
            for element in els:
                collection_field_list = filter(lambda x: x == element.text, iter(colls))
                if len(collection_field_list) > 0:
                    return bool(1)
        return bool(0)

    def extract_local_metadata(self, record):
        # type: (Element) -> Element
        """
        This method extracts the metadata to add metadata_local.xml in the saf directory.
        Data fields are mapped to the local metadata registry configured for our dspace instance.

        :param record: etree Element representing the contentdm record.
        :return: a new etree Element representing data that will be written to metadata_local.xml.
        """
        cdm_structure = Fields.cdm_structural_elements
        dspace_local = Fields.dspace_local_field
        dspace_local_map = FieldMaps.local_field_map

        metadata_local = ET.Element('dublin_core')
        metadata_local.set('schema', 'local')

        cdmfullResolution = record.iterfind(cdm_structure['preservation_location'])
        # This should probably be considered a hack.
        cdmunmapped = record.iterfind(ExtractMetadata.cdm_dc['unmapped'])

        # TODO: the eadid needs to be mapped to a unique field. For now, use string match so some eadid fields will
        #  appear in dspace.
        for element in cdmunmapped:
            if element.text is not None:
                if element.text.find('WUA') != -1:
                    relation_references = ET.SubElement(metadata_local, 'dcvalue')
                    relation_references.set('element', dspace_local['eadid'])
                    relation_references.text = element.text

        self.__process_iterable_map(metadata_local, cdmfullResolution, dspace_local_map)
        self.extract_page.add_page_admin_data(metadata_local, record)

        return metadata_local

    def extract_metadata(self, record):
        # type: (Element) -> Element
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.

        :param record: the etree Element for the contentdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        dspace_dc = Fields.dspace_dc_field
        dc_field_map = FieldMaps.dc_field_map

        dublin_core = ET.Element('dublin_core')
        dublin_core.set('schema', 'dc')

        # Because this uses sorted keys, the field order is alphabetical.
        cdm_keys = sorted(ExtractMetadata.cdm_dc.keys())
        for key in cdm_keys:
            if key in cdm_keys:
                elements = record.iterfind(ExtractMetadata.cdm_dc[key])
                if key == ExtractMetadata.cdm_dc['format']:
                    if not self.is_single_item(record) and not self.should_process_compound_as_single(record):
                         # Sets the format element for compound objects.
                        cpdformat = ET.SubElement(dublin_core, 'dcvalue')
                        cpdformat.set('element', dspace_dc['format'])
                        cpdformat.text = 'Compound'

                        # Rather than rely on the CONTENTdm notion of a compound object
                        # to control our application logic, we should add a new field --
                        # relation:requires -- and use it to specify the data repository
                        # that is required to view the item. Currently, this is 'existdb'
                        # The initial batch of test records was exported without this element.
                        require_relation = ET.SubElement(dublin_core, 'dcvalue')
                        require_relation.set('element', dspace_dc['relation'])
                        require_relation.set('qualifier', dspace_dc['require_relation'])
                        require_relation.text = 'existdb'

                    else:
                        self.__process_iterable_map(dublin_core, elements, dc_field_map)
                else:
                    self.__process_iterable_map(dublin_core, elements, dc_field_map)

        return dublin_core
