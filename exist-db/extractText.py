#!/usr/bin/env python
import xml.etree.ElementTree as ET

def extractText(filename):
	file = open(filename,'r')
	id = filename[9:-4]
	tree = ET.parse(file)
	root = tree.getroot()
	pages = root.findall('./pages/page/fullText/body')
	holder = '';
	for page in pages:

		# surpisingly using a space here spaces the 
     		# hyphenated node from the rest of the line.
		holder += ' '.join(page.itertext())
	
	return holder
