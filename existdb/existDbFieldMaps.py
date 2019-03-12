#!/usr/bin/env python

from existDbFields import ExistDbFields


class ExistDbFieldMaps:
    """Mapping for existdb to DSpace dublin core and local fields.
    """

    def __init__(self):
        pass

    mets_structural_elements = ExistDbFields.mets_structural_elements
    processor_field = ExistDbFields.processor_mods_elements
    dspace_dc_field = ExistDbFields.dspace_dc_field

    # Defines how to map mets metadata to dspace dublin core.
    mods_field_map = {

        mets_structural_elements['label_attr']: {
            'element': dspace_dc_field['title'],
            'qualifier': None
        },
        processor_field['date_issued_element']: {
            'element': dspace_dc_field['date'],
            'qualifier': None
        },
        processor_field['identifier_element']: {
            'element': 'identifier',
            'qualifier': None
        },
        processor_field['resource_type_element']: {
            'element': dspace_dc_field['type'],
            'qualifier': None
        },
        processor_field['access_conditions_element']: {
            'element': dspace_dc_field['rights'],
            'qualifier': None
        },
        processor_field['language_element']: {
            'element': dspace_dc_field['language'],
            'qualifier': None
        },
        processor_field['physical_extent_element']: {
            'element': dspace_dc_field['format'],
            'qualifier': dspace_dc_field['format_extent_qualifier'],
        },
        processor_field['note_element']: {
            'element': dspace_dc_field['source'],
            'qualifier': None
        },
        processor_field['item_details_element']: {
            'element': 'identifier',
            'qualifier': 'citation'
        }
    }


