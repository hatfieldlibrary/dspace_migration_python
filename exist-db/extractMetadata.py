#!/usr/bin/env python

import xml.etree.ElementTree as ET

def extractMetadata(filename):

        file = open(filename,'r')
        id = filename[15:-4]
	tree = ET.parse(file)
	root = tree.getroot()
	title = root[0].text
	print title
	vol = root[1].text
	issue = root[2].text
	date = root[3].text
	top = ET.Element('dublin_core');
	# top.set('schema','dc')
	titleEL = ET.SubElement(top, 'dcvalue')
	titleEL.set('element','title')
	titleEL.text = title;
	volumeEL = ET.SubElement(top, 'dcvalue')
        volumeEL.set('element','description')
	volumeEL.text = vol
        issueEL = ET.SubElement(top, 'dcvalue')
        issueEL.set('element','description')
	issueEL.text = issue;
        dateEL = ET.SubElement(top, 'dcvalue')
        dateEL.set('element','date')
	dateEL.set('qualifier','issued')
	dateEL.text = date
	identifierEL = ET.SubElement(top, 'dcvalue')
	identifierEL.set('element','identifier')
	identifierEL.text = id
	return top	
