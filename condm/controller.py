#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET

from collection_config import CollectionConfig
from collection_processor import CollectionProcessor


class ContentdmController:

    error_count = 0

    def __init__(self, collection, input_file, output_directory):
        """
        Constructor.
        :type output_directory: str
        :type input_file: str
        :type collection: str
        :param collection: the Contentdm collection name (e.g. aphotos)
        :param input_file: the xml file exported from Contentdm
        :param output_directory: The parent saf output directory
        """
        self.collection = collection
        self.input = input_file
        self.output = output_directory

    def process_collections(self):
        """
        Process contentdm collections. This uses the collection configuration
        for sub-collections. For records that have a recognized sub-collection
        in the expected DC field, a sub-collection processor is used. Otherwise,
        a base processor is used. Each processor directs output to the
        saf directory defined in the collection configuration.
        """
        base_directory = os.getcwd()
        # The input file.
        input_file = base_directory + '/condm/data/' + self.input

        cdm_collection = CollectionConfig.sub_collection_mapping[self.collection]
        sub_collections = cdm_collection['field_values']

        # The parent output directory.
        base_out_dir = base_directory + '/condm/saf/' + self.output

        base_processor = CollectionProcessor(self.collection, base_out_dir)

        collection_map = {}
        for sub_collection in sub_collections:
            out_dir = base_out_dir + '/' + sub_collection['dspace_out']
            collection_processor = CollectionProcessor(self.collection, out_dir)
            collection_map[sub_collection['cdm_collection']] = collection_processor

        # open the input file for reading.
        input_xml = open(input_file, 'r')

        # Parse the input file and gather the 'record' nodes.
        tree = ET.parse(input_xml)
        root = tree.getroot()
        records = root.findall('./record')

        for record in records:

            collection_field_value = record.find(cdm_collection['field_name'])
            processor = collection_map[collection_field_value]
            if processor is not None:
                processor.process_record(record)
            else:
                print 'Collection processor not found for ' + collection_field_value
                base_processor.process_record(record)



