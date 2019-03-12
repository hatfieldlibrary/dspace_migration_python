#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET
from io import open

from extractMetadata import ExtractMetadata
from extractExistFullText import ExtractExistFullText
from shared.utils import Utils


class ExistController:

	def __init__(self, collection, input_file, output_directory):
		"""
		Constructor.

		:type output_directory: str
		:type input_file: str
		:type collection: str
		:param collection: the Contentdm collection name (e.g. aphotos)
		:param input_file: the xml file exported from Contentdm
		:param output_directory: The parent simple archive format output directory
		"""
		self.collection = collection
		self.input = input_file
		self.output = output_directory

	def process_records(self):
		"""
		This is the top-level method for processing Contentdm records.
		It initializes the processing environment, parses the xml input file,
		and iterates over records, maintaining state for the current working
		directory (e.g. saf/archives_images/batch_1) and current saf item
		directory (e.g. item_0010/).  Other processing tasks are delegated
		to imported classes.
		"""
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

			# Each working directory will contain 1000 items.
			# The working directories are labelled batch_1, batch_2 ...
			if counter % 1000 == 0:
				counter = 0
				batch += 1
				working_dir = Utils.init_working_directory(out_dir, batch)

			# Create the working directory
			current_dir = Utils.int_saf_sub_directory(working_dir, counter)

			# Extract metadata
			dc_metadata = metadata_extractor.extract_metadata(root)

			# Write as xml
			tree = ET.ElementTree(dc_metadata)
			tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

			# Extract the full text
			fulltext = page_data_extractor.extract_text(os.path.join(text_dir + '/' + item))

			# For utf-8 output we need to use the io library open function. With python3 this can be done
			# using the default python open func. (I'm using python 2.7)
			try:
				# Write fulltext
				with open(current_dir + '/file_1.txt', 'w', encoding='UTF-8') as file2:
					file2.write(unicode(fulltext))
					file2.close()
			except IOError as err:
				error_count += 1
				print('An error occurred writing full text data to saf for: %s. See %s'%(doc_title, current_dir))
				print('IO Error: {0}'.format(err))
			except AssertionError as err:
				error_count += 1
				print('An error occurred writing full text for: %s. See %s'%(doc_title, current_dir))
				print 'AssertionError: {0}'.format(err)

			try:
				# Add text file to the saf contents file.
				with open(current_dir + '/contents', 'w') as file3:
					file3.write(unicode('file_1.txt'))
					file3.close()
			except IOError as err:
				error_count += 1
				print('An error occurred writing contents to saf for: %s. See %s'%(doc_title, current_dir))
				print('IO Error: {0}'.format(err))
			except Exception as err:
				error_count += 1
				print('An error occurred writing contents for: %s. See %s'%(doc_title, current_dir))
				print 'Exception: {0}'.format(err)

			counter += 1

		# Done.
		final_count = Utils.get_final_count(batch, counter)

		print('%s records loaded'%str(final_count))

		if error_count > 0:
			print'%s errors!'%str(error_count)


