import os
import xml.etree.ElementTree as ET

iiif_enabled = '<?xml version="1.0" encoding="UTF-8"?><dublin_core schema="dspace"><dcvalue element="iiif" ' \
               'qualifier="enabled">true</dcvalue></dublin_core> '

iiif_search = '<?xml version="1.0" encoding="UTF-8"?><dublin_core schema="iiif"><dcvalue element="search" ' \
              'qualifier="enabled">true</dcvalue></dublin_core> '


class AddMetadata:

    def __init__(self, saf_directory):
        self.saf_directory = saf_directory

    def add_metadata(self):
        base_directory = os.path.abspath(os.getcwd())
        in_dir = base_directory + '/existdb/saf/' + self.saf_directory + '/batch_1'

        for saf_dir in os.listdir(in_dir):
            current_dir = in_dir + '/' + saf_dir

            dc_tree = ET.ElementTree(ET.fromstring(iiif_enabled))
            dc_tree.write(current_dir + '/metadata_dspace.xml', encoding="UTF-8", xml_declaration=True)

            dc_tree = ET.ElementTree(ET.fromstring(iiif_search))
            dc_tree.write(current_dir + '/metadata_iiif.xml', encoding="UTF-8", xml_declaration=True)
