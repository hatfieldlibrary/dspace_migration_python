

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

    sub_collection_mapping = {
        'aphotos': {
            'field_name': 'source',
            'field_values': [
                {
                    'cdm_collection': 'Postcard Collection',
                    'dspace_out': 'postcard_collection'
                },
                {
                    'cdm_collection': 'Helen Pearce Collection',
                    'dspace_out': 'pearce_collection'
                }
            ]
        }
    }
