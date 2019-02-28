#!/usr/bin/env python

import os
from extractMetadata import ExtractMetadata
from fetchBitstreams import FetchBitstreams
from extractPageData import ExtractPageData
from utils import Utils

import xml.etree.ElementTree as ET


class ContentdmController:

	def __init__(self, collection, input_file, output_directory):
		"""
		Constructor.
		:param collection: the Contentdm collection name (e.g. aphotos)
		:param input_file: the xml file exported from Contentdm
		:param output_directory: The parent simple archive format output directory
		"""
		self.collection = collection
		self.input = input_file
		self.output = output_directory

	def processRecords(self):
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
		file1 = base_directory + '/condm/data/' + self.input
		# The parent output directory.
		out_dir = base_directory + '/condm/saf/' + self.output

		utils = Utils(out_dir)
		metadata_extractor = ExtractMetadata()
		page_data_extractor = ExtractPageData()

		counter = 0
		batch = 0
		working_dir = ''

		# open the input file for reading.
		input_xml = open(file1, 'r')

		# Parse the input file and gather the 'record' nodes.
		tree = ET.parse(input_xml)
		root = tree.getroot()
		records = root.findall('./record')

		for record in records:
	
			# Each working directory will contain 1000 items.
			# The working directories are labelled batch_1, batch_2 ...
			if counter % 1000 == 0:
				counter = 0
				batch += 1
				working_dir = utils.initWorkingDirectory(batch)
			
			# Create a new saf item sub-directory inside the working directory
			current_dir = utils.intSafSubDirectory(working_dir, counter)

			# Capture dc metadata and write to archive
			dc_metadata = metadata_extractor.extractMetadata(record)
			tree = ET.ElementTree(dc_metadata)
			tree.write(current_dir + '/dublin_core.xml', encoding="UTF-8", xml_declaration="True")

			if metadata_extractor.isSingleItem(record):
				# single item, not a compound object!
				try:
					# Get bitstreams for single item and add to archives
					FetchBitstreams.fetchBitStreams(current_dir, record, self.collection)
				except RuntimeError as err:					print(err)

			else:
				# A compound object.
				# Create full-text file for compound object and add to saf directory.
				extext = page_data_extractor.extractText(record)
				file2 = open(current_dir + '/file_1.txt', 'w')
				file2.write(extext)
				file3 = open(current_dir + '/contents', 'w')
				file3.write('file_1.txt')
				file2.close()
				file3.close()

				# This should be called after the full-text file has been added.
				# It will retrieve the thumbnail for the compound object.
				FetchBitstreams.fetchThumbnailOnly(current_dir, record, self.collection)

			counter += 1


			# Extract and write metadata to be imported via our local dspace schema.
			local_metadata = metadata_extractor.extractLocalMetadata(record)
			tree = ET.ElementTree(local_metadata)
			tree.write(current_dir + '/metadata_local.xml', encoding="UTF-8", xml_declaration="True")

		final_count = utils.getFinalCount(batch, counter)
		print('%s records loaded'%(str(final_count)))
