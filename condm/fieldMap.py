#!/usr/bin/env python

class FieldMaps:

    # Fields as they are exported by CONTENTdm
    cdmField = {
        'id': 'cdmid',
        'filename': 'cdmfile',
        'thumbnail': 'thumbnailURL',
        'preservation_location': 'fullResolution',
        'compound_object_container': 'structure',
        'compound_object_page': 'page',
        'compound_object_page_title': 'pagetitle',
        'compound_object_page_file': 'pagefile',
        'compound_object_page_file_type': 'pagefiletype',
        'compound_object_page_file_loc': 'pagefilelocation',
        'compound_object_page_text': 'pagetext',
        'unmapped': 'unmapped',
        'title': 'title',
        'creator': 'creator',
        'description': 'description',
        'alt_title': 'alternative',
        'subject': 'subject',
        'coverage_spatial': 'spatial',
        'date': 'date',
        'format': 'format',
        'publisher': 'publisher',
        'source': 'source',
        'identifier': 'identifier',
        'date_created': 'cdmcreated',
        'language': 'language',
        'medium': 'medium',
        'extent': 'extent',
        'is_part_of': 'isPartOf',
        'format': 'format',
        'rights': 'rights',
        'relation': 'relation',
        'provenance': 'provenance',
        'publisher': 'publisher',
        'type': 'type',
    }

    # Map fields for DSpace import
    dspaceField = {
        'eadid': 'EADID',
        'preservation_location': 'mastercopy',
        'title': 'title',
        'title_alt_qualifier': 'alternative',
        'creator': 'creator',
        'description': 'description',
        'description_provenance_qualifier': 'provenance',
        'date': 'date',
        'date_created_qualifier': 'created',
        'subject': 'subject',
        'source': 'source',
        'relation': 'relation',
        'relation_uri_qualifier': 'uri',
        'relation_ispartof_qualifier': 'ispartof',
        'relation_isformatof_qualifier': 'isformatof',
        'coverage': 'coverage',
        'coverage_spatial_qualifier': 'spatial',
        'language': 'language',
        'identifier': 'identifier',
        'publisher': 'publisher',
        'type': 'type',
        'format': 'format',
        'format_medium_qualifier': 'medium',
        'format_extent_qualifier': 'extent',
        'rights': 'rights'

    }

    def getCdmFieldMap(self):
        return self.cdmField

    def getDspaceFieldMap(self):
        return self.dspaceField
