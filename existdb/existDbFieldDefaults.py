#!/usr/bin/env python

from existDbFields import ExistDbFields


class DefaultFieldValueMap:

    def __init__(self):
        pass

    processor_fields = ExistDbFields.processor_mods_elements

    # Use this dictionary to add default values. If an element does not exist in the existdb
    # mets the default value will be added to the dspace import xml.
    default_values = {
        processor_fields['language_element']: {
            'value': 'English',
            'attr': None,
            'attr_val': None
        },
        processor_fields['access_conditions_element']: {
            'value': 'All rights reserved by Willamette University',
            'attr': None,
            'attr_val': None

        },
        processor_fields['resource_type_element']: {
            'value': 'text',
            'attr': None,
            'attr_val': None
        },
        processor_fields['statement_responsibility_element']: {
            # note:type='statement of responsibility'
            'value': 'Willamette University',
            'attr': 'statement of responsibility',
            'attr_val': 'statementofresponsibility'
        }
    }
