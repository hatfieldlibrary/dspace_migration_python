#!/usr/bin/env python

import xml.etree.ElementTree as ET
from extractPageData import ExtractPageData
from fieldMap import FieldMaps


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
        if elements is not None:
                for element in elements:
                    if element.text is not None:
                        dspace_element = element_map[element.tag]
                        sub_element = ET.SubElement(parent_element, 'dcvalue')
                        sub_element.set('element', dspace_element['element'])
                        if dspace_element['qualifier'] is not None:
                            sub_element.set('qualifier', dspace_element['qualifier'])
                        sub_element.text = element.text


    def extractLocalMetadata(self, record):
        """
        This method extracts metadata to add to the metadata_local.xml file in the saf directory.
        The extracted fields will be mapped to fields in the local metadata registry configured
        for our dspace instance.
        :param record: etree Element representing the contentdm record.
        :return: a new etree Element representing data that will be written to metadata_local.xml.
        """
        fields = FieldMaps()
        cdm = fields.getCdmFieldMap()
        dspace = fields.getDspaceFieldMap()

        top = ET.Element('dublin_core')
        top.set('schema', 'local')

        cdmfullResolution = record.find(cdm['preservation_location'])
        cdmunmapped = record.iterfind(cdm['unmapped'])

        # TODO: this needs to be mapped to a unique metadata field.
        for element in cdmunmapped:
            if element.text is not None:
                if element.text.find('WUA') != -1:
                    relation_references = ET.SubElement(top, 'dcvalue')
                    relation_references.set('schema', 'local')
                    relation_references.set('element', dspace['eadid'])
                    relation_references.text = element.text

        if cdmfullResolution is not None:
            if cdmfullResolution.text is not None:
                res_el = ET.SubElement(top, 'dcvalue')
                res_el.set('schema', 'local')
                res_el.set('element', dspace['preservation_location'])
                res_el.text = cdmfullResolution.text

        self.extract_page.addPageAdminData(top, record)

        return top

    def extractMetadata(self, record):
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.
        :param record: the etree Element for the contentdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        fields = FieldMaps()
        cdm = fields.getCdmFieldMap()
        dspace = fields.getDspaceFieldMap()
        field_map = fields.getCdmToDspaceMap()

        cdmtitle = record.iterfind(cdm['title'])
        cdmalternatives = record.iterfind(cdm['alt_title'])
        cdmcreators = record.iterfind(cdm['creator'])
        cdmdescriptions = record.iterfind(cdm['description'])
        cdmsubjects = record.iterfind(cdm['subject'])
        cdmspatial = record.iterfind(cdm['coverage_spatial'])
        cdmdates = record.iterfind(cdm['date'])
        cdmsources = record.iterfind(cdm['source'])
        cdmidentifiers = record.iterfind(cdm['identifier'])
        cdmdate_created = record.iterfind(cdm['date_created'])
        cdmlanguage = record.iterfind(cdm['language'])
        cdmisPartOf = record.iterfind(cdm['relation_ispartof'])
        cdmformats = record.iterfind(cdm['format'])
        cdmrights = record.iterfind(cdm['rights'])
        cdmrelations = record.iterfind(cdm['relation'])
        cdmprovenance = record.iterfind(cdm['provenance'])
        cdmpublishers = record.iterfind(cdm['publisher'])
        cdmtypes = record.iterfind(cdm['type'])
        cdmextents = record.iterfind(cdm['format_extent'])
        cdmmediums = record.iterfind(cdm['format_medium'])

        top = ET.Element('dublin_core')
        top.set('schema', 'dc')

        self.processIterableMap(top, cdmtitle, field_map)
        self.processIterableMap(top, cdmalternatives, field_map)
        self.processIterableMap(top, cdmcreators, field_map)
        self.processIterableMap(top, cdmdescriptions, field_map)
        self.processIterableMap(top, cdmdates, field_map)

        if cdmrelations is not None:
            for rel in cdmrelations:
                if rel.text is not None:
                    relEL = ET.SubElement(top, 'dcvalue')
                    relEL.set('element', dspace['relation'])
                    if (rel.text.find('http') != -1):
                        relEL.set('qualifier', dspace['relation_qualifier_uri'])
                    relEL.text = rel.text

        self.processIterableMap(top, cdmspatial, field_map)
        self.processIterableMap(top, cdmsubjects, field_map)
        self.processIterableMap(top, cdmisPartOf, field_map)
        self.processIterableMap(top, cdmlanguage, field_map)
        self.processIterableMap(top, cdmdate_created, field_map)
        self.processIterableMap(top, cdmidentifiers, field_map)
        self.processIterableMap(top, cdmpublishers, field_map)
        self.processIterableMap(top, cdmrights, field_map)
        self.processIterableMap(top, cdmprovenance, field_map)
        self.processIterableMap(top, cdmtypes, field_map)
        self.processIterableMap(top, cdmsources, field_map)
        self.processIterableMap(top, cdmmediums, field_map)
        self.processIterableMap(top, cdmextents, field_map)

        if not self.isSingleItem(record):
            # sets the format for compound objects
            cpdformat = ET.SubElement(top, 'dcvalue')
            cpdformat.set('element', dspace['format'])
            cpdformat.text = 'Compound'
        else:
            self.processIterableMap(top, cdmformats, field_map)

        return top
