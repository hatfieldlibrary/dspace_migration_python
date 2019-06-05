

class CollectionConfig:

    # This class is for collection level configuration.

    def __init__(self):
        pass

    # Collections that contain contentdm compound objects that should be loaded
    # into dspace as single items that contain more than one bitstream (e.g. postcards).
    collections_to_omit_compound_objects = {
        'aphotos': {
            'field_name': 'type',
            'field_values': [
                'postcards'
            ]
        }
    }
