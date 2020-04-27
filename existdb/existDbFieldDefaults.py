#!/usr/bin/env python

from .existDbFields import ExistDbFields
from .existDbFieldMaps import ExistDbFieldMaps

class DefaultFieldValueMap:

    def __init__(self):
        pass

    dspace_dc_fields = ExistDbFields.dspace_dc_field
    switch_tag = ExistDbFieldMaps.switch_tag

    # Use this dictionary to add default values. If an element does not exist in the existdb
    # mets the default value will be added to the dspace import xml.
    default_values = {
        dspace_dc_fields['language']: {
            'value': 'English',
            'attr': None,
            'attr_val': None
        },
        dspace_dc_fields['rights']: {
            'value': 'All rights reserved by Willamette University',
            'attr': None,
            'attr_val': None

        },
        dspace_dc_fields['type']: {
            'value': 'text',
            'attr': None,
            'attr_val': None
        },
        dspace_dc_fields['description_statement_of_responsibility']: {
            # note:type='statement of responsibility'
            'value': 'Willamette University',
            'attr': 'statement of responsibility',
            'attr_val': 'statementofresponsibility'
        }
    }
