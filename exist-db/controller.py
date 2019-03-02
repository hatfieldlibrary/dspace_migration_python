#!/usr/bin/env python

import os
import xml.etree.ElementTree as ET

from extractMetadata import ExtractMetadata
from extractPageData import ExtractPageData
from utils import Utils


class ContentdmController:

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
		# The input file.
		file1 = base_directory + '/exist-db/data/' + self.input
		# The parent output directory.
		out_dir = base_directory + '/exist-db/saf/' + self.output

		metadata_extractor = ExtractMetadata()
		page_data_extractor = ExtractPageData()

		counter = 0
		batch = 0
		working_dir = ''
		error_count = 0

		# open the input file for reading.
		input_xml = open(file1, 'r')

		# Parse the input file and gather the 'record' nodes.
		tree = ET.parse(input_xml)
		root = tree.getroot()
		records = root.findall('./record')

		for record in records:

			doc_title = record.find('title').text

			# Each working directory will contain 1000 items.
			# The working directories are labelled batch_1, batch_2 ...
			if counter % 1000 == 0:
				counter = 0
				batch += 1
				working_dir = Utils.init_working_directory(out_dir, batch)

			# Create a new saf item sub-directory inside the working directory
			current_dir = Utils.int_saf_sub_directory(working_dir, counter)

			# Capture dc metadata and write to archive
			dc_metadata = metadata_extractor.extract_metadata(record)
			tree = ET.ElementTree(dc_metadata)
			tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

			try:

				# A compound object.
				# Create full-text file for compound object and add to saf directory.
				extext = page_data_extractor.extract_text(record)
				file2 = open(current_dir + '/file_1.txt', 'w')
				file2.write(extext)
				file3 = open(current_dir + '/contents', 'w')
				file3.write('file_1.txt')
				file2.close()
				file3.close()
			except IOError as err:
				error_count += 1
				print('An error occurred writing compound object data to saf for: %s. See %s'%(doc_title, current_dir))
				print('IO Error: {0}'.format(err))
			except:
				error_count += 1
				print('An error occurred writing compound object data to saf: %s. See %s'%(doc_title, current_dir))

			# Extract and write metadata to be imported via our local dspace schema.
			local_metadata = metadata_extractor.extract_local_metadata(record)
			tree = ET.ElementTree(local_metadata)

			try:
				tree.write(current_dir + '/metadata_local.xml', encoding="UTF-8", xml_declaration="True")
			except IOError as err:
				error_count += 1
				print('An error occurred writing local metadata for: %s. See %s'%(doc_title, current_dir))
				print('IO Error: {0}'.format(err))
			except:
				error_count += 1
				print('An error occurred writing local metadata for: %s. See %s'%(doc_title, current_dir))

			counter += 1

		final_count = Utils.get_final_count(batch, counter)

		print('%s records loaded'%str(final_count))

		if error_count > 0:
			print'%s errors!'%str(error_count)
