#!/usr/bin/env python

class FieldMaps:

    # THE FIRST 4 DICTIONARIES DESCRIBE THE DC AND LOCAL ELEMENTS USED BY CDM AND DSPACE.

    # DC fields as they are exported by CONTENTdm. Includes "unmapped".
    cdm_dc_field = {
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

    # Non-dc (e.g. structural) xml elements exported by cdm.
    cdm_structural_elements = {
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
        'compound_object_page_text': 'pagetext'
    }

    # Fields used for DSpace dublin core import
    dspace_dc_field = {
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

    # Fields for dspace local metadata import.
    dspace_local_field = {
        'eadid': 'EADID',
        'preservation_location': 'mastercopy'
    }

    # THE FOLLOWING DICTIONARIES CONTROL HOW CDM RECORDS ARE IMPORTED INTO DSPACE.

    # This dictionary maps cdm to dspace dublin core.
    dc_field_map = {

        cdm_dc_field['title']: {
            'element': dspace_dc_field['title'],
            'qualifier': None
        },
        cdm_dc_field['alt_title']: {
            'element': dspace_dc_field['title'],
            'qualifier': dspace_dc_field['title_alt_qualifier']
        },
        cdm_dc_field['creator']: {
            'element': dspace_dc_field['creator'],
            'qualifier': None
        },
        cdm_dc_field['description']: {
            'element': dspace_dc_field['description'],
            'qualifier': None
        },
        cdm_dc_field['date']: {
            'element': dspace_dc_field['date'],
            'qualifier': None
        },
        cdm_dc_field['date_created']: {
            'element': dspace_dc_field['date'],
            'qualifier': dspace_dc_field['date_created_qualifier']
        },
        cdm_dc_field['coverage_spatial']: {
            'element': dspace_dc_field['coverage'],
            'qualifier': dspace_dc_field['coverage_spatial_qualifier']
        },
        cdm_dc_field['subject']: {
            'element': dspace_dc_field['subject'],
            'qualifier': None
        },
        # From archives_images: <relation>http://archiveswest.orbiscascade.org/ark:/80444/xv81204</relation>
        # Could be mapped to dsapce relation.uri. If that's what we need, then cdm field mapping should
        # be changed so we can easily identify the field after export.
        cdm_dc_field['relation']: {
            'element': dspace_dc_field['relation'],
            'qualifier': None
        },
        cdm_dc_field['relation_ispartof']: {
            'element': dspace_dc_field['relation'],
            'qualifier': dspace_dc_field['relation_ispartof_qualifier']
        },
        cdm_dc_field['language']: {
            'element': dspace_dc_field['language'],
            'qualifier': None
        },
        cdm_dc_field['identifier']: {
            'element': dspace_dc_field['identifier'],
            'qualifier': None
        },
        cdm_dc_field['publisher']: {
            'element': dspace_dc_field['publisher'],
            'qualifier': None
        },
        cdm_dc_field['rights']: {
            'element': dspace_dc_field['rights'],
            'qualifier': None
        },
        cdm_dc_field['provenance']: {
            'element': dspace_dc_field['description'],
            'qualifier': dspace_dc_field['description_provenance_qualifier']
        },
        cdm_dc_field['type']: {
            'element': dspace_dc_field['type'],
            'qualifier': None
        },
        cdm_dc_field['source']: {
            'element': dspace_dc_field['source'],
            'qualifier': None
        },
        cdm_dc_field['format']: {
            'element': dspace_dc_field['format'],
            'qualifier': None
        },
        cdm_dc_field['format_medium']: {
            'element': dspace_dc_field['format'],
            'qualifier': dspace_dc_field['format_medium_qualifier']
        },
        cdm_dc_field['format_extent']: {
            'element': dspace_dc_field['format'],
            'qualifier': dspace_dc_field['format_extent_qualifier']
        }
    }

    # This dictionary maps cdm to dspace LOCAL metadata.
    local_field_map = {
        cdm_structural_elements['preservation_location']: {
            'element': dspace_local_field['preservation_location'],
            'qualifier': None
        },
        # Currently exported from cdm as unmapped.
        cdm_dc_field['unmapped']: {
            'element': dspace_local_field['eadid'],
            'qualifier': None
        }
    }

