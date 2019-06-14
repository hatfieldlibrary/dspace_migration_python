#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET
from io import open

from analyzer import ExistAnalyzer
from extractMetadata import ExtractMetadata
from extractExistFullText import ExtractExistFullText
from fetchThumbnail import FetchThumbnailImage
from shared.utils import Utils


class ExistController:

    def __init__(self, collection, input_dir, output_directory, dry_run):
        """
        Constructor.

        :type output_directory: str
        :type input_dir: str
        :type collection: str
        :param collection: the exist collection name (e.g. collegian)
        :param input_dir: the directory that contains mets and fulltext sub-directories
        :param output_directory: The parent simple archive format output directory
        """
        self.collection = collection
        self.input = input_dir
        self.output = output_directory
        self.dry_run = dry_run
        self.analyzer = ExistAnalyzer()

    def process_records(self):
        """
        This is the top-level method for processing exisdb mets records.
        It initializes the processing environment, parses the xml input file,
        and iterates over records, maintaining state for the current working
        directory (e.g. saf/collegian/batch_1) and current saf item
        directory (e.g. item_0010/).  Other processing tasks are delegated
        to imported classes.
        """

        # NOTE: existdb records are exported without a thumbnail. For
        # display purposes, we may want to add a default thubmnail image
        # to the saf subdirectories. In dspace, these thumbnail bitstreams
        # would create a lot of redundancy (same image over and over) but
        # it might turn out to be the sanest way to handle UI concerns.

        base_directory = os.getcwd()
        # The input mets directory.
        in_dir = base_directory + '/existdb/data/' + self.input + '/mets'
        # The input fulltext directory
        text_dir = base_directory + '/existdb/data/' + self.input + '/fulltext'
        # The parent output directory.
        out_dir = base_directory + '/existdb/saf/' + self.output

        counter = 0
        batch = 0
        working_dir = ''
        error_count = 0

        metsList = os.listdir(in_dir)
        for item in metsList:
            # read each file in the mets directory.
            metsFile = open(os.path.join(in_dir + '/' + item), 'r')

            # Parse the input file
            tree = ET.parse(metsFile)
            root = tree.getroot()

            # The document title is useful for error messages.
            doc_title = root.attrib['LABEL']

            # Get extractor instances.
            metadata_extractor = ExtractMetadata()
            page_data_extractor = ExtractExistFullText()
            fetch_thumbnail_utility = FetchThumbnailImage(self.analyzer)

            # Each working directory will contain 1000 items.
            # The working directories are labelled batch_1, batch_2 ...
            if counter % 1000 == 0:
                counter = 0
                batch += 1
                if not self.dry_run:
                    working_dir = Utils.init_working_directory(out_dir, batch)

            current_dir = ''
            if not self.dry_run:
                # Create the working directory
                current_dir = Utils.int_saf_sub_directory(working_dir, counter)  # type: str

            # The convention for exisb-db mets files is to append '01' at the end of the string.
            # For series, the file name without the appended value equals the dateIssued, and
            # this is how we look up items:
            #
            #   fn:replace($mets//mods:dateIssued[not(@qualifier)], '-', '')
            #
            # For title-based items, the mets:OBJID value is used. This value again equals the
            # file name with the final '01' removed from the string:
            #
            #   OBJID="NormaPaulusScrapbook04"
            #
            # So here, derive the item id from the file name and pass it to the extract_metadata()
            # function.

            # removing \d\d.xml
            item_id = item[:-6]

            # Temporary hack for Wallulah processing. Should not be needed with updated fulltext file names.
            # item = item_id + '.xml'

            # Extract metadata
            dc_metadata = metadata_extractor.extract_metadata(root, item_id)
            # Extract the full text
            fulltext = page_data_extractor.extract_text(os.path.join(text_dir + '/' + item))
            # For the image path, remove only the xml extension.
            image_path = item[:-4]
            fetch_thumbnail_utility.fetch_thumbnail(root, self.collection, image_path, current_dir, self.dry_run)

            if not self.dry_run:
                # Write as xml
                tree = ET.ElementTree(dc_metadata)
                tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

            # For utf-8 output we need to use the io library open function. With python3 this can be done
            # using the default python open func. (I'm using python 2.7)
            try:
                if not self.dry_run:
                    # Write fulltext
                    with open(current_dir + '/file_1.txt', 'w', encoding='UTF-8') as file2:
                        file2.write(unicode(fulltext))
                        file2.close()
            except IOError as err:
                error_count += 1
                print('An error occurred writing full text data to saf for: %s. See %s' % (doc_title, current_dir))
                print('IO Error: {0}'.format(err))
            except AssertionError as err:
                error_count += 1
                print('An error occurred writing full text for: %s. See %s' % (doc_title, current_dir))
                print 'AssertionError: {0}'.format(err)

            try:
                if not self.dry_run:
                    # Add text file to the saf contents file.
                    with open(current_dir + '/contents', 'a') as file3:
                        file3.write(unicode('file_1.txt'))
                        file3.close()
            except IOError as err:
                error_count += 1
                print('An error occurred writing contents to saf for: %s. See %s' % (doc_title, current_dir))
                print('IO Error: {0}'.format(err))
            except Exception as err:
                error_count += 1
                print('An error occurred writing contents for: %s. See %s' % (doc_title, current_dir))
                print 'Exception: {0}'.format(err)

            counter += 1

        # Done.
        final_count = Utils.get_final_count(batch, counter)

        print('%s records loaded' % str(final_count))

        if error_count > 0:
            print'%s errors!' % str(error_count)

        print ('Image processing failed for:')
        self.analyzer.print_image_encoding_failures()

