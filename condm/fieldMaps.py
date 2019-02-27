#!/usr/bin/env python

from fields import Fields


class FieldMaps:
    """Mapping for CONTENTdm to DSpace dublin core and local fields.

    Dictionaries in the class define how CONTENTdm fields are mapped to DSpace qualified Dublin Core
    and to local metadata fields defined in the DSpace metadata registry.
    """

    def __init__(self):
        pass

    cdm_dc_field = Fields.cdm_dc_field
    cdm_structural_elements = Fields.cdm_structural_elements
    dspace_dc_field = Fields.dspace_dc_field
    dspace_local_field = Fields.dspace_local_field

    # This dictionary maps cdm to dspace DUBLIN CORE.

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
