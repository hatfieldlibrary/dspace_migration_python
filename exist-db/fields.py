#!/usr/bin/env python


class Fields:
    """This class manages field names used by DSpace and METS.

    Dictionaries define field names used for mods, mets strucutral metadata, and dspace dublin core and local fields
    defined in the DSpace metadata registry.
    """
    def __init__(self):
        pass

    # DC fields as they are exported by CONTENTdm. Includes "unmapped".
    mets_mods_field = {
        'identifier_element': 'mods:identifier',
        'doi_type_attr': 'doi',
        'item_details_element': 'mods:detail',
        'type_attr': 'type',
        'date_issued_element': 'mods:dateIssued',
        'date_encoding_attr': 'encoding',
        'note_element': 'mods:note',
        'access_conditions_element': 'mods:accessCondition',
        'language_element': 'mods:languageTerm',
        'language_code_attr': 'code',
        'language_authority_attr': 'authority',
        'title_element': 'mods:title',
        'sub_title_element': 'mods:subTitle',
        'physical_description_element': 'mods:physicalDescription',
        'physical_extent_element': 'mods:extent',
        'resource_type_element': 'mods:typeOfResource'
    }

    # mets structural elements and attributes
    mets_structural_elements = {
        'mets_header_element': 'mets:metsHdr',
        'mets_agent_element': 'mets:agent',
        'mets_agent_name_element': 'mets:name',
        'descriptive_metadata_section_element': 'mets:dmdSec',
        'mods_section_element': 'mods:mods'
    }

    composite_values = {
        'citation': 'citation'
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
        'citation_qualifier': 'citation',
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


