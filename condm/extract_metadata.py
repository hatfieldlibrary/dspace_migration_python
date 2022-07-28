import xml.etree.ElementTree as ET
from collections import Iterable
from xml.etree.ElementTree import Element

from .extract_page_data import ExtractPageData
from .custom_format_field import CustomFormatField
from .fields import Fields
from .collection_config import CollectionConfig
from .fieldMaps import FieldMaps
from shared.utils import Utils


class ExtractMetadata:
    cdm_dc = Fields.cdm_dc_field
    cdm_struc = Fields.cdm_structural_elements

    def __init__(self):
        self.extract_page = ExtractPageData()
        self.custom_format_field = CustomFormatField()

    def add_elements(self, parent_element, element_map, element):
        """
        Adds new element to parent
        :param parent_element:
        :param element_map:
        :param element:
        :return: None
        """
        if element.text == 'Willamette University Archives and Special Collections':
            element.text = 'Willamette University Archives'

        if element.tag == 'subject' or element.tag == 'level':
            subjects = element.text.split(';')
            for subject in subjects:
                element.text = subject
                self.add_element(parent_element, element_map, element)
        else:
            self.add_element(parent_element, element_map, element)

    @staticmethod
    def add_element(parent_element, element_map, element):
        dspace_element = element_map[element.tag]
        sub_element = ET.SubElement(parent_element, 'dcvalue')
        sub_element.set('element', dspace_element['element'])
        if dspace_element['qualifier'] is not None:
            sub_element.set('qualifier', dspace_element['qualifier'])
        # correct text encoding before adding to the new element
        sub_element.text = Utils.correct_text_encoding(element.text)

    def process_iterable_map(self, parent_element, elements, element_map, add_master=False):
        # type: (Element, Iterable, dict, bool) -> None
        """
        Processes a list of etree elements using
        a CONTENTdm to DSpace field map. This method adds new sub-elements to the
        parent element (which will later be written to the saf dublin_core.xml).

        :param parent_element: the parent etree Element to which sub-elements will be added.
        :param elements: the list of etree elements to read.
        :param element_map: the dictionary for cdm to dspace mapping.
        :param add_master: (optional) set value to True to process preservation locations (allows you to add fields
        at end of the list)
        """
        if elements is not None:
            for element in elements:
                if element.text is not None:
                    # exclude unmapped fields
                    if element.tag != ExtractMetadata.cdm_dc['unmapped']:
                        if element.tag == 'title':
                            print(element.text)
                        if element.tag in element_map:
                            if add_master:
                                # Add preservation location if available.
                                if element.tag == ExtractMetadata.cdm_struc['preservation_location']:
                                    self.add_elements(parent_element, element_map, element)
                            else:
                                # Add all non-preservation metadata.
                                if element.tag != ExtractMetadata.cdm_struc['preservation_location']:
                                    self.add_elements(parent_element, element_map, element)
                        # process custom format.extent fields
                        if element.tag in Fields.format_extent_fields:
                            self.custom_format_field.add_format(Fields.format_extent_fields[element.tag], element.text)

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
    def should_process_compound_as_single(record, collection):
        """
        Checks to see if a compound object record should be treated as a single item. Call
        this function before processing a contentdm compound object record.
        :param record: etree Element representing the contentdm record.
        :param collection: the contentdm collection name
        :return: true if the value in the collection id field is found in the list collection configuration
                array for items that do not need to be loaded as compound objects (e.g. postcards)
        """
        if record.find(CollectionConfig.collections_to_omit_compound_objects[collection]['field_name']) is not None:
            # If the field name is allSubCollections then the entire parent collection should process compound
            # objects as single items.
            if record.find(CollectionConfig.collections_to_omit_compound_objects[collection]['field_name']) == \
                    'allSubCollections':
                return bool(1)
            # Check check for sub-collections defined in field_values.
            colls = CollectionConfig.collections_to_omit_compound_objects[collection]['field_values']
            els = record.findall(CollectionConfig.collections_to_omit_compound_objects[collection]['field_name'])
            for element in els:
                collection_field_filter = filter(lambda x: x == element.text, iter(colls))
                if collection_field_filter is not None:
                    collection_field_list = list(collection_field_filter)
                    if len(collection_field_list) > 0:
                        return bool(1)
        return bool(0)

    def add_compound_object_local_metadata(self, record, collection, local):
        # type: (Element, str, Element) -> None
        """
        Adds a new objecttype and dependency fields to local metadata. These are used
        to mark records that will use existdb for item views.
        :param record: etree Element representing the contentdm record.
        :param collection: the current collection name
        :param local: the local metadata element
        """

        dspace_local_map = Fields.dspace_local_field
        if not self.is_single_item(record) and not \
                self.should_process_compound_as_single(record, collection):
            cpdformat = ET.SubElement(local, 'dcvalue')
            cpdformat.set('element', dspace_local_map['object_type'])
            cpdformat.text = 'Compound'
            # Rather than rely on the CONTENTdm notion of a compound object
            # to control application logic, we should add a new local field --
            # dependency -- and use it to specify the data repository
            # that is hosts the item data. Currently, this is 'existdb'
            # require_relation = ET.SubElement(local, 'dcvalue')
            # require_relation.set('element', dspace_local_map['dependency'])
            # require_relation.text = 'existdb'

    def extract_local_metadata(self, record, collection):
        # type: (Element, str) -> Element
        """
        This method extracts dspace local metadata.

        :param record: etree Element representing the contentdm record.
        :param collection the contentdm collection name
        :return: a new etree Element representing data that will be written to metadata_local.xml.
        """
        dspace_local_map = FieldMaps.local_field_map

        metadata_local = ET.Element('dublin_core')
        metadata_local.set('schema', 'local')

        # Process metadata for dspace local fields (this will include the preservation copy for single items)
        # Passing the entire record twice. Could be more efficient.
        # Add all local field except preservation location.
        self.process_iterable_map(metadata_local, record, dspace_local_map)
        # Append preservation locations at the end of the field list.
        # This has no effect on DSpace (display order is determined by the field id number!). But it's nice
        # to append at the end of the field list for review prior to DSpace import.
        self.process_iterable_map(metadata_local, record, dspace_local_map, True)
        # Add custom local metadata fields for compound objects.
        self.add_compound_object_local_metadata(record, collection, metadata_local)
        # Extract preservation data from compound object page elements.
        self.extract_page.add_page_admin_data(metadata_local, record)

        return metadata_local

    def extract_metadata(self, record):
        # type: (Element) -> Element
        """
        Extracts data that will be added to the dublin_core.xml file in the saf item directory.

        :param record: the etree Element for the CONTENTdm record.
        :return: an etree Element containing dublin core metadata that will be written to the saf dublin_core.xml file.
        """
        dc_field_map = FieldMaps.dc_field_map
        dublin_core = ET.Element('dublin_core')
        dublin_core.set('schema', 'dc')

        cdm_keys = sorted(ExtractMetadata.cdm_dc.keys())
        for key in cdm_keys:
            if ExtractMetadata.cdm_dc[key] in dc_field_map:
                elements = record.iterfind(ExtractMetadata.cdm_dc[key])
                self.process_iterable_map(dublin_core, elements, dc_field_map)
        # Some records need custom format.extent
        self.custom_format_field.add_custom_format_element(dublin_core)

        return dublin_core
