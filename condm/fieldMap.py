#!/usr/bin/env python

class FieldMaps:

    # This class defines dictionaries for CONTENTdm fields, DSpace fields, and
    # mapping between the two systems.

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
        'format_medium': 'medium',
        'format_extent': 'extent',
        'relation_ispartof': 'isPartOf',
        'rights': 'rights',
        'relation': 'relation',
        'provenance': 'provenance',
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

    # Use this dictionary to map contentdm and dspace fields.
    field_map = {

        cdmField['title']: {
            'element': dspaceField['title'],
            'qualifier': None
        },
        cdmField['alt_title']: {
            'element': dspaceField['title'],
            'qualifier': dspaceField['title_alt_qualifier']
        },
        cdmField['creator']: {
            'element': dspaceField['creator'],
            'qualifier': None
        },
        cdmField['description']: {
            'element': dspaceField['description'],
            'qualifier': None
        },
        cdmField['date']: {
            'element': dspaceField['date'],
            'qualifier': None
        },
        cdmField['date_created']: {
            'element': dspaceField['date'],
            'qualifier': dspaceField['date_created_qualifier']
        },
        cdmField['coverage_spatial']: {
            'element': dspaceField['coverage'],
            'qualifier': dspaceField['coverage_spatial_qualifier']
        },
        cdmField['subject']: {
            'element': dspaceField['subject'],
            'qualifier': None
        },
        cdmField['relation_ispartof']: {
            'element': dspaceField['relation'],
            'qualifier': dspaceField['relation_ispartof_qualifier']
        },
        cdmField['language']: {
            'element': dspaceField['language'],
            'qualifier': None
        },
        cdmField['identifier']: {
            'element': dspaceField['identifier'],
            'qualifier': None
        },
        cdmField['publisher']: {
            'element': dspaceField['publisher'],
            'qualifier': None
        },
        cdmField['rights']: {
            'element': dspaceField['rights'],
            'qualifier': None
        },
        cdmField['provenance']: {
            'element': dspaceField['description'],
            'qualifier': dspaceField['description_provenance_qualifier']
        },
        cdmField['type']: {
            'element': dspaceField['type'],
            'qualifier': None
        },
        cdmField['source']: {
            'element': dspaceField['source'],
            'qualifier': None
        },
        cdmField['format']: {
            'element': dspaceField['format'],
            'qualifier': None
        },
        cdmField['format_medium']: {
            'element': dspaceField['format'],
            'qualifier': dspaceField['format_medium_qualifier']
        },
        cdmField['format_extent']: {
            'element': dspaceField['format'],
            'qualifier': dspaceField['format_extent_qualifier']
        }
    }

    def getCdmFieldMap(self):
        return self.cdmField

    def getDspaceFieldMap(self):
        return self.dspaceField

    def getCdmToDspaceMap(self):
            return self.field_map
