#!/usr/bin/env python

from fields import Fields


class FieldMaps:
    """Mapping for CONTENTdm to DSpace dublin core and local fields.

    Dictionaries in the class define how CONTENTdm fields are mapped to DSpace qualified Dublin Core
    and to local metadata fields defined in the DSpace metadata registry.
    """

    def __init__(self):
        pass

    mods_field = Fields.mets_mods_field
    composites = Fields.composite_values;
    cdm_structural_elements = Fields.mets_structural_elements
    dspace_dc_field = Fields.dspace_dc_field
    dspace_local_field = Fields.dspace_local_field

    # This dictionary maps cdm to dspace DUBLIN CORE.

    mods_field_map = {

        mods_field['title_element']: {
            'element': dspace_dc_field['title'],
            'qualifier': None
        },
        mods_field['sub_title_element']: {
            'element': dspace_dc_field['title'],
            'qualifier': dspace_dc_field['title_alt_qualifier']
        },
        # mods_field['creator']: {
        #     'element': dspace_dc_field['creator'],
        #     'qualifier': None
        # },
        # mods_field['description']: {
        #     'element': dspace_dc_field['description'],
        #     'qualifier': None
        # },
        mods_field['date_issued_element']: {
            'element': dspace_dc_field['date'],
            'qualifier': None
        },
        # mods_field['date_created']: {
        #     'element': dspace_dc_field['date'],
        #     'qualifier': dspace_dc_field['date_created_qualifier']
        # },
        # mods_field['coverage_spatial']: {
        #     'element': dspace_dc_field['coverage'],
        #     'qualifier': dspace_dc_field['coverage_spatial_qualifier']
        # },
        composites['citation']: {
            'element': dspace_dc_field['identifier'],
            'qualifier': dspace_dc_field['citation_qualifier']
        },
        mods_field['access_conditions_element']: {
            'element': dspace_dc_field['rights'],
            'qualifier': None
        },
        mods_field['language_element']: {
            'element': dspace_dc_field['language'],
            'qualifier': dspace_dc_field['relation_ispartof_qualifier']
        },
        mods_field['language']: {
            'element': dspace_dc_field['language'],
            'qualifier': None
        },
        mods_field['extent']: {
            'element': dspace_dc_field['format'],
            'qualifier': dspace_dc_field['format_extent_qualifier'],
        },
        mods_field['publisher']: {
            'element': dspace_dc_field['publisher'],
            'qualifier': None
        },
        # mods_field['rights']: {
        #     'element': dspace_dc_field['rights'],
        #     'qualifier': None
        # },
        # # Dspace creates it's own decription.provenance at import.
        # mods_field['provenance']: {
        #     'element': dspace_dc_field['description'],
        #     'qualifier': dspace_dc_field['description_provenance_qualifier']
        # },
        # mods_field['type']: {
        #     'element': dspace_dc_field['type'],
        #     'qualifier': None
        # },
        # mods_field['source']: {
        #     'element': dspace_dc_field['source'],
        #     'qualifier': None
        # },
        # mods_field['format']: {
        #     'element': dspace_dc_field['format'],
        #     'qualifier': None
        # },
        # mods_field['format_medium']: {
        #     'element': dspace_dc_field['format'],
        #     'qualifier': dspace_dc_field['format_medium_qualifier']
        # },
        # mods_field['format_extent']: {
        #     'element': dspace_dc_field['format'],
        #     'qualifier': dspace_dc_field['format_extent_qualifier']
        # }
    }

    # This dictionary maps cdm to dspace LOCAL metadata.

    local_field_map = {
        cdm_structural_elements['preservation_location']: {
            'element': dspace_local_field['preservation_location'],
            'qualifier': None
        },
        # Currently exported from cdm as unmapped.
        mods_field['unmapped']: {
            'element': dspace_local_field['eadid'],
            'qualifier': None
        }
    }
