
import re
import xml.etree.ElementTree as ET

from .analyzer import Analyzer
from .extract_metadata import ExtractMetadata
from .fetch_bitstreams import FetchBitstreams
from .extract_page_data import ExtractPageData
from shared.utils import Utils


class CollectionProcessor:

    error_count = 0
    counter = 0
    batch = 0
    working_dir = ''
    dry_run = False
    analyzer = None
    text_file = 'file_1.txt'

    def __init__(self, parent_collection, output_directory, analyzer, dry_run):
        """
        Constructor.
        :type parent_collection: str
        :type output_directory: str
        :param parent_collection: the name of the contentdm collection (e.g. aphotos)
        :param output_directory: the saf output directory for this sub-collection
        """
        self.parent_collection = parent_collection
        self.output = output_directory
        print(self.output)
        self.dry_run = dry_run
        assert isinstance(analyzer, Analyzer), "%r is not a print queue" % analyzer
        self.analyzer = analyzer
        self.fetch_bitstreams = FetchBitstreams()

    def extract_full_text(self, record, current_dir, doc_title, page_data_extractor):
        # type (Element, str, str, ExtractPageData) -> bool
        """
        Attempts to extract full text from a compound object record and writes
        data to saf directory if found. Returns True if full text was found.
        :param record: the exported contentdm record
        :param current_dir: the output directory
        :param doc_title: the title of the item
        :param page_data_extractor: an instance of the extractor class.
        :return:
        """
        regex = re.compile('[a-z]')
        try:
            # A compound object.
            # Create full-text file for compound object and add to saf directory.
            full_text_data = page_data_extractor.extract_text(record)
            if regex.search(full_text_data) is not None:
                file2 = open(current_dir + '/' + self.text_file, 'w')
                file2.write(full_text_data)
                file2.close()
                return True

        except IOError as err:
            CollectionProcessor.error_count += 1
            print('An error occurred writing compound object data to saf for: %s. See %s' % (
                doc_title, current_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            CollectionProcessor.error_count += 1
            print('An error occurred writing compound object data to saf: %s. See %s' % (
                doc_title, current_dir))
            print('Exception: {0}'.format(err))

    def write_contents_file(self, current_dir, doc_title):
        # type (str, str) -> None
        """
        Writes the full text file name (file_1.txt) to the saf contents file.
        :param current_dir: output directory
        :param doc_title: title of the record being processed.
        """
        try:
            self.fetch_bitstreams.append_to_contents(current_dir, doc_title, 'fulltext')

        except IOError as err:
            CollectionProcessor.error_count += 1
            print('An error occurred writing the saf contents for: %s. See %s' % (doc_title, current_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            CollectionProcessor.error_count += 1
            print('An error occurred writing the saf contents for: %s. See %s' % (doc_title, current_dir))
            print('Exception: {0}'.format(err))

    # @staticmethod
    # def append_contents_file(current_dir, doc_title):
    #     # type (str, str) -> None
    #     """
    #      Appends the full text file name (file_1.txt) to the saf contents file.
    #     :param current_dir: output directory
    #     :param doc_title: title of the record being processed.
    #     """
    #     try:
    #         FetchBitstreams.append_to_contents(current_dir, doc_title, 'fulltext')
    #
    #     except IOError as err:
    #         CollectionProcessor.error_count += 1
    #         print('An error occurred writing the saf contents for: %s. See %s' % (doc_title, current_dir))
    #         print('IO Error: {0}'.format(err))
    #     except Exception as err:
    #         CollectionProcessor.error_count += 1
    #         print('An error occurred writing the saf contents for: %s. See %s' % (doc_title, current_dir))
    #         print('Exception: {0}'.format(err))

    def generate_saf(self, record):
        """
        This is the top-level method for processing Contentdm records.
        It initializes the processing environment, parses the xml input file,
        and iterates over records, maintaining state for the current working
        directory (e.g. saf/archives_images/batch_1) and current saf item
        directory (e.g. item_0010/).  Other processing tasks are delegated
        to imported classes.
        """

        metadata_extractor = ExtractMetadata()
        page_data_extractor = ExtractPageData()

        # Each working directory will contain 1000 items.
        # The working directories are labelled batch_1, batch_2 ...
        if self.counter % 1000 == 0:
            self.counter = 0
            self.batch += 1
            self.working_dir = Utils.init_working_directory(self.output, self.batch)
            print(self.working_dir)

        doc_title = record.find('title').text

        # Create a new saf item sub-directory inside the working directory
        current_dir = Utils.int_saf_sub_directory(self.working_dir, self.counter)

        # Capture dc metadata and write to archive
        dc_metadata = metadata_extractor.extract_metadata(record)

        tree = ET.ElementTree(dc_metadata)
        tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

        # This is a single item, not a compound object!
        if metadata_extractor.is_single_item(record):
            print('single record')
            try:
                # Get bitstreams for single item and add to archives
                self.fetch_bitstreams.fetch_bit_streams(current_dir, record, self.parent_collection, False)

            except RuntimeError as err:
                CollectionProcessor.error_count += 1
                print(err)
            except IOError as err:
                CollectionProcessor.error_count += 1
                print('An error occurred retrieving bitstreams for: %s. See %s' % (doc_title, current_dir))
                print('IO Error: {0}'.format(err))
            except Exception as err:
                CollectionProcessor.error_count += 1
                print('An error occurred retrieving bitstreams for: %s. See %s' % (doc_title, current_dir))
                print('Exception: {0}'.format(err))

        elif metadata_extractor.should_process_compound_as_single(record, self.parent_collection):
            print('compound record')
            # This is a compound object that will be processed as a single item.
            try:
                self.fetch_bitstreams.fetch_bit_streams(current_dir, record, self.parent_collection, True)

            except RuntimeError as err:
                self.error_count += 1
                print(err)
            except IOError as err:
                self.error_count += 1
                print('An error occurred retrieving bitstreams for: %s. See %s' % (doc_title, current_dir))
                print('IO Error: {0}'.format(err))
            except Exception as err:
                self.error_count += 1
                print('An error occurred retrieving bitstreams for: %s. See %s' % (doc_title, current_dir))
                print('Exception: {0}'.format(err))

            # extract full text and add to saf directory
            found_text = self.extract_full_text(record, current_dir, doc_title, page_data_extractor)
            if found_text:
                print('single')
                # Appends to the saf contents file after bitstreams have been added.
                self.write_contents_file(current_dir, self.text_file)
        else:
            print('compound record 2')
            # This is a compound object.
            # Extract full text and add it to saf directory
            found_text = self.extract_full_text(record, current_dir, doc_title, page_data_extractor)
            if found_text:
                print('compound')
                print(found_text)
                # Writes to first line of saf contents file before the thumbnail is retrieved.
                self.write_contents_file(current_dir, self.text_file)
            # Get a thumbnail image.

            # try:
            #     # This should be called after the full-text file has been added.
            #     # It will retrieve the thumbnail for the compound object.
            #     FetchBitstreams.fetch_thumbnail_only(current_dir, record, self.parent_collection)
            #
            # except IOError as err:
            #     self.error_count += 1
            #     print('An error occurred retrieving thumbnail for: %s. See %s' % (doc_title, current_dir))
            #     print('IO Error: {0}'.format(err))
            # except Exception as err:
            #     self.error_count += 1
            #     print('An error occurred retrieving thumbnail for: %s. See %s' % (doc_title, current_dir))
            #     print('Exception: {0}'.format(err))

        self.counter += 1

        # Extract and write metadata to be imported into our local metadata fields.
        local_metadata = metadata_extractor.extract_local_metadata(record, self.parent_collection)
        tree = ET.ElementTree(local_metadata)

        # Add DSpace IIIF metadata
        iiif_enabled = '<?xml version="1.0" encoding="UTF-8"?><dublin_core schema="dspace"><dcvalue element="iiif" ' \
                       'qualifier="enabled">true</dcvalue></dublin_core> '
        ds_tree = ET.ElementTree(ET.fromstring(iiif_enabled))

        # Set the canvas name prefix to "Image"
        iiif_naming = '<?xml version="1.0" encoding="UTF-8"?><dublin_core schema="iiif"><dcvalue element="canvas" ' \
                      'qualifier="naming">Image</dcvalue></dublin_core> '
        naming_tree = ET.ElementTree(ET.fromstring(iiif_naming))

        try:
            tree.write(current_dir + '/metadata_local.xml', encoding="UTF-8", xml_declaration=True)
            ds_tree.write(current_dir + '/metadata_dspace.xml', encoding="UTF-8", xml_declaration=True)
            naming_tree.write(current_dir + '/metadata_iiif.xml', encoding="UTF-8", xml_declaration=True)

        except IOError as err:
            self.error_count += 1
            print('An error occurred writing local metadata for: %s. See %s' % (doc_title, current_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            self.error_count += 1
            print('An error occurred writing local metadata for: %s. See %s' % (doc_title, current_dir))
            print('Exception: {0}'.format(err))

    def process_record(self, record):
        if self.dry_run:
            metadata_extractor = ExtractMetadata()
            if metadata_extractor.is_single_item(record):
                self.analyzer.add_single_item()
            elif metadata_extractor.should_process_compound_as_single(record, self.parent_collection):
                self.analyzer.add_multiple_item_record()
            else:
                el = record.find("title")
                self.analyzer.add_compound_object()
        else:
            self.generate_saf(record)
