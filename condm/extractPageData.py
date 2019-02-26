#!/usr/bin/env python

import xml.etree.ElementTree as ET
from fieldMap import FieldMaps


class ExtractPageData:

    def __init__(self):
        pass

    def addPageAdminData(self, top, record):
        """
        Adds master file location for each page to the metadata_local.xml saf output file.
        :param top: the dublin_core (local schema) element
        :param record: the etree element for the contentdm record
        """
        fields = FieldMaps()
        cdm = fields.getCdmFieldMap()
        dspace = fields.getDspaceFieldMap()

        structure_el = record.find(cdm['compound_object_container'])
        pages_el = structure_el.iterfind('.//' + cdm['compound_object_page'])

        for page in pages_el:

            title = page.find(cdm['compound_object_page_title'])
            page_files = page.iterfind(cdm['compound_object_page_file'])
            for file_el in page_files:
                type_el = file_el.find(cdm['compound_object_page_file_type'])
                if type_el.text == 'master':
                    file_location = file_el.find(cdm['compound_object_page_file_loc'])
                    master_el = ET.SubElement(top, 'dcvalue')
                    master_el.set('element', dspace['preservation_location'])
                    if file_location.text is not None:
                        master_el.text = title.text + ' master: ' + file_location.text

    def extractText(self, record):
        """
        Returns full text extracted from cdm compound object pages.
        :param record: the etree element for the cdm record.
        :return: the full text of the item
        """
        fields = FieldMaps()
        cdm = fields.getCdmFieldMap()

        structure_el = record.find(cdm['compound_object_container'])
        pages_el = structure_el.iterfind('.//' + cdm['compound_object_page'])
        fulltext = ''
        for page in pages_el:
            page_el = page.find(cdm['compound_object_page_text'])
            if page_el is not None:
                if page_el.text is not None:
                    fulltext += page_el.text

        return fulltext