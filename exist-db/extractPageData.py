#!/usr/bin/env python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from condm.utils import Utils
from fields import Fields


class ExtractPageData:

	def __init__(self):
		pass

	def add_page_admin_data(self, top, record):
		# type: (Element, Element) -> None
		"""
        Adds master file location for each page to the metadata_local.xml saf output file.

        :param top: the dublin_core (local schema) element
        :param record: the etree element for the contentdm record
        """
		cdm_struc = Fields.mets_structural_elements
		dspace_local = Fields.dspace_local_field

		structure_el = record.find(cdm_struc['compound_object_container'])
		pages_el = structure_el.iterfind('.//' + cdm_struc['compound_object_page'])

		for page in pages_el:
			title = page.find(cdm_struc['compound_object_page_title'])
			page_files = page.iterfind(cdm_struc['compound_object_page_file'])
			for file_el in page_files:
				type_el = file_el.find(cdm_struc['compound_object_page_file_type'])
				if type_el.text == 'master':
					file_location = file_el.find(cdm_struc['compound_object_page_file_loc'])
					master_el = ET.SubElement(top, 'dcvalue')
					master_el.set('element', dspace_local['preservation_location'])
					if file_location.text is not None:
						master_el.text = title.text + ' master: ' + file_location.text

	def extract_text(self, record):
		# type: (Element) -> str
		"""
        Returns full text extracted from cdm compound object pages.

        :param record: the etree element for the cdm record.
        :return: the full text of the item
        """
		cdm_struc = Fields.mets_structural_elements

		structure_el = record.find(cdm_struc['compound_object_container'])
		pages_el = structure_el.iterfind('.//' + cdm_struc['compound_object_page'])
		fulltext = ''
		for page in pages_el:
			page_el = page.find(cdm_struc['compound_object_page_text'])
			if page_el is not None:
				if page_el.text is not None:
					page_el = Utils.correct_text_encoding(page_el)
					fulltext += page_el.text

		return fulltext
