#!/usr/bin/env python
import os
import extractText as text
import extractMetadata as meta
import xml.etree.ElementTree as ET

path = 'export9'

try:
	os.mkdir(path)
except OSError:
	print("Unable to create the %s directory" % path)
else:
	print("Created the %s directory" % path)

files = ['1920s/fulltext/1923051601.xml','1920s/fulltext/1927020901.xml','1920s/fulltext/1928040501.xml']
counter = 0

for filename in files:
	os.mkdir(path + '/item_00' + str(counter))
	extext = text.extractText(filename)
	exmeta = meta.extractMetadata(filename)
	file = open(path + '/item_00' + str(counter) + '/dublin_core.xml','w')
	file.write(ET.tostring(exmeta))
	file2 = open(path + '/item_00' + str(counter) + '/file_1.txt','w')
	file2.write(extext)
	file3 = open(path + '/item_00' + str(counter) + '/contents','w')
	file3.write('file_1.txt')
	counter+=1
	file.close()
	file2.close()
	file3.close()
	

