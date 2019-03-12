#!/usr/bin/env python

from existDbFields import ExistDbFields


class DefaultFieldValueMap:

    def __init__(self):
        pass

    mods_fields = ExistDbFields.processor_mods_elements

    # Use this dictionary to add default values. If an element does not exist in the existdb
    # mets the default value will be added to the dspace import xml.
    default_values = {
        mods_fields['language_element']: {
            'value': 'English'
        },
        mods_fields['access_conditions_element']: {
            'value': 'All rights reserved by Willamette University'
        },
        mods_fields['resource_type_element']: {
            'value': 'text'
        },
        mods_fields['note_element']: {
            # note:type='statement of responsibility'
            'value': 'Willamette University'
        }
    }