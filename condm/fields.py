#!/usr/bin/env python


class Fields:
    """This class manages field names used by DSpace and CONTENTdm.

    Dictionaries define field names used for Dublin Core, non-Dublin Core CONTENTdm fields, and local fields
    defined in the DSpace metadata registry.
    """
    def __init__(self):
        pass

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


