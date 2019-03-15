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

    # Dspace mapping keys can be mets elements (e.g. dateIssued) or unique
    # keys defined below.
    switch_tag = {
        'statement_of_responsibility': {
            # Use this key to lookup DC mapping for statement of responsibility.
            # This is read from the mods:note element in the mets file. It maps
            # to description:statementofresponsibility in dspace.
            'id': 'statement_of_responsibility'
        },
        'exist_db_id': {
            # Use this key to look up DC dspace mapping for the item id.
            # This value is either derived for the publication date or taken
            # directly from the mets:LABEL attribute.
            'id': 'exist_db_id'
        },
        'database_relation': {
            # This field does not exist in the mets file. We add it to all
            # items as relation:requires with the value 'existdb'. It
            # will be used to tell the dspace angular client where item
            # can be found.  (We could also embed the base or full url here.)
            'id': 'uses_exist_db_relation'
        }
    }

    # Defines how to map mets metadata values to dspace dublin core.
    ds_field_map = {

        mets_structural_elements['label_attr']: {
            'element': dspace_dc_field['title'],
            'qualifier': None
        },
        processor_field['date_issued_element']: {
            'element': dspace_dc_field['date'],
            'qualifier': dspace_dc_field['date_issued_qualifier']
        },
        # Maps the database id (existdb) to relation:requires.
        switch_tag['database_relation'].get('id'): {
            'element': dspace_dc_field['relation'],
            'qualifier': dspace_dc_field['relation_requires']
        },
        processor_field['identifier_element']: {
            'element': 'identifier',
            'qualifier': None
        },
        # Maps item identifier to identifier:other (for the exist item id).
        switch_tag['exist_db_id'].get('id'): {
            'element': dspace_dc_field['identifier'],
            'qualifier': dspace_dc_field['identifier_exist_id_attr']
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
        # Maps mets "note" with type "statement of responsibility" to description:statementofresponsibility
        switch_tag['statement_of_responsibility'].get('id'): {
            'element': dspace_dc_field['description'],
            'qualifier': dspace_dc_field['description_statement_responsibility_qualifier']
        },
        processor_field['item_details_element']: {
            'element': 'identifier',
            'qualifier': 'citation'
        }
    }


