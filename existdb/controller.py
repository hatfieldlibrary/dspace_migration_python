#!/usr/bin/env python

import os, shutil
import xml.etree.ElementTree as ET
from io import open

from fetchPdfFiles import FetchPdfFiles
from .analyzer import ExistAnalyzer
from .extractMetadata import ExtractMetadata
from .extractExistFullText import ExtractExistFullText
from .fetchThumbnail import FetchThumbnailImage
from .fetchPageImage import FetchPageImages
from .fetchAltoFiles import FetchAltoFiles
from shared.utils import Utils


class ExistProcessor:

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

        base_directory = os.path.abspath(os.getcwd())
        # The input mets directory.
        in_dir = base_directory + '/existdb/data/' + self.input + '/mets'
        # The input fulltext directory
        text_dir = base_directory + '/existdb/data/' + self.input + '/fulltext'
        # The input alto directory
        alto_dir = base_directory + '/existdb/data/' + self.input + '/alto'
        # The input pdf directory
        pdf_dir = base_directory + '/existdb/data/' + self.input + '/pdf'
        # The parent output directory.
        out_dir = base_directory + '/existdb/saf/' + self.output

        counter = 0
        batch = 0
        working_dir = ''
        error_count = 0

        # process each file in the mets directory.
        for item in os.listdir(in_dir):

            mets_file = open(os.path.join(in_dir + '/' + item), 'rt')

            mets_dirs = mets_file.name.split("/")
            mets_name = mets_dirs[len(mets_dirs) - 1]

            # Parse the input file
            mets_tree = ET.parse(mets_file)

            root = mets_tree.getroot()

            # The document title is useful for error messages.
            doc_title = root.attrib['LABEL']
            # This is the base for ALTO (and perhaps other) files. Required for retrieving from database.
            # If using the mets.xml file for indexing order, you'll probably need to modify the file name
            # using the fetchAltoFiles cut_size.
            if 'OBJID' in root.attrib:
                # Used for non-serials (see comment below)
                obj_id = root.attrib['OBJID']
            else:
                # More typical value, based on the file name
                obj_id = item[:-6]

            # Get extractor instances.
            metadata_extractor = ExtractMetadata()
            page_data_extractor = ExtractExistFullText()
            fetch_thumbnail_utility = FetchThumbnailImage(self.analyzer)
            fetch_page_images = FetchPageImages(self.analyzer)
            fetch_alto_files = FetchAltoFiles(self.analyzer)
            fetch_pdf_files = FetchPdfFiles(self.analyzer)

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

            if not self.dry_run:
                # Write as xml
                dc_tree = ET.ElementTree(dc_metadata)
                dc_tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

            if not self.dry_run:
                # mets_file_path = mets_file.name
                # shutil.copy(mets_file_path, current_dir)
                # mets_dirs = mets_file_path.split("/")
                # mets_name = mets_dirs[len(mets_dirs) - 1]
                # dst_file = os.path.join(current_dir, mets_name)
                original_file_name = mets_file.name
                dst_file = os.path.join(current_dir, 'mets.xml')
                os.rename(original_file_name, dst_file)
                with open(current_dir + '/contents', 'a') as content2:
                    # content2.write(mets_name + '\tbundle:OtherContent\n')
                    # Use this whenever possible (file name 'mets.xml')
                    content2.write('mets.xml\tbundle:OtherContent\n')
                    content2.close()

                # try:
                #     if not self.dry_run:
                #         # Add text file to the saf contents file.
                #         with open(current_dir + '/contents', 'a') as file3:
                #             file3.write(str('fulltext_1.txt\tbundle:OtherContent\n'))
                #             file3.close()
                # except IOError as err:
                #     error_count += 1
                #     print('An error occurred writing contents to saf for: %s. See %s' % (doc_title, current_dir))
                #     print('IO Error: {0}'.format(err))
                # except Exception as err:
                #     error_count += 1
                #     print('An error occurred writing contents for: %s. See %s' % (doc_title, current_dir))
                #     print('Exception: {0}'.format(err))

            if not self.dry_run:
                fetch_alto_files.fetch_files(root, self.collection, obj_id, current_dir, self.dry_run)

                try:
                    if not self.dry_run:
                        # Write fulltext
                        with open(current_dir + '/fulltext_1.txt', 'w', encoding='UTF-8') as file2:
                            file2.write(fulltext)
                            file2.close()
                        with open(current_dir + '/contents', 'a') as content2:
                            content2.write('fulltext_1.txt\tbundle:OtherContent\n')
                            content2.close()

                except IOError as err:
                    error_count += 1
                    print('An error occurred writing fulltext to saf for: %s. See %s' % (doc_title, current_dir))
                    print('IO Error: {0}'.format(err))
                except AssertionError as err:
                    error_count += 1
                    print('An error occurred writing fulltext for: %s. See %s' % (doc_title, current_dir))
                    print('AssertionError: {0}'.format(err))

            # For the image path, remove only the xml extension.
            image_path = item[:-4]
            if not self.dry_run:
                fetch_thumbnail_utility.fetch_thumbnail(root, self.collection, image_path, current_dir, self.dry_run)

            if not self.dry_run:
                # Watch out for this, collections may vary.
                pdf_base = mets_name[:-4]
                pdf_name = pdf_base + '.pdf'
                fetch_pdf_files.fetch_files(pdf_name, self.collection, current_dir, self.dry_run)

            if not self.dry_run:
                fetch_page_images.fetch_images(root, self.collection, image_path, current_dir, self.dry_run)

            counter += 1
            mets_file.close()
            print('.', end='')

        # Done.
        print(os.stat(in_dir + '/' + item))
        final_count = Utils.get_final_count(batch, counter)

        print('\n%s records loaded' % str(final_count))

        if error_count > 0:
            print('\n%s errors!' % str(error_count))

        self.analyzer.print_image_encoding_failures()
        self.analyzer.print_alto_processing_failures()

