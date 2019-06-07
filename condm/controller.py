#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET

from analyzer import Analyzer
from collection_config import CollectionConfig
from collection_processor import CollectionProcessor
from shared.utils import Utils


class ContentdmController:

    error_count = 0
    analyzer = None

    def __init__(self, collection, input_file, output_directory, dry_run):
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
        self.dry_run = dry_run
        self.analyzer = Analyzer()

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
        parent_out_dir = base_directory + '/condm/saf/' + self.output

        base_out_dir = parent_out_dir + '/base'
        base_processor = CollectionProcessor(self.collection, base_out_dir, self.analyzer, self.dry_run)
        if not self.dry_run:
            Utils.init_sub_collection_directory(base_out_dir)

        collection_map = {}
        for sub_collection in sub_collections:
            if sub_collection['load']:
                out_dir = parent_out_dir + '/' + sub_collection['dspace_out']
                if not self.dry_run:
                    Utils.init_sub_collection_directory(out_dir)
                collection_processor = CollectionProcessor(self.collection, out_dir, self.analyzer, self.dry_run)
                collection_map[sub_collection['cdm_collection']] = {
                    'processor': collection_processor,
                    'load': sub_collection['load']
                }
            else:
                if self.dry_run:
                    self.analyzer.excluded_collection(sub_collection['cdm_collection'])

        # open the input file for reading.
        input_xml = open(input_file, 'r')

        # Parse the input file and gather the 'record' nodes.
        tree = ET.parse(input_xml)
        root = tree.getroot()
        records = root.findall('./record')

        count = 0
        for record in records:

            collection_field_value_el = record.find(cdm_collection['field_name'])
            collection_field_value = collection_field_value_el.text
            if collection_field_value in collection_map:
                processor = collection_map[collection_field_value]['processor']
                if collection_map[collection_field_value]['load']:
                    processor.process_record(record)
                if self.dry_run:
                    self.analyzer.sub_collection(collection_field_value)
            else:
                base_processor.process_record(record)
                if self.dry_run:
                    self.analyzer.unprocessed_collection(collection_field_value)

            count += 1

        if self.dry_run:
            print '\nSUB-COLLECTIONS'
            self.analyzer.print_sub_collection_rpt()
            self.analyzer.print_unprocessed_collection_rpt()
            self.analyzer.print_excluded_collection_rpt()

            print '\nITEM TYPES'
            self.analyzer.print_item_type_report()
            print('\n%s records processed in dry run of %s' % (str(count), self.output))

        if not self.dry_run:
            print('\n%s records loaded into %s' % (str(count), self.output))
            print 'To see more load information use the --dry-run flag.'
