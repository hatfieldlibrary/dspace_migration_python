

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
                    'dspace_out': 'postcard_collection',
                    'load': True
                },
                {
                    'cdm_collection': 'Helen Pearce Collection',
                    'dspace_out': 'pearce_collection',
                    'load': True
                },
                {
                    'cdm_collection': 'Campus Photographs',
                    'dspace_out': 'campus_photographs',
                    'load': True
                },
                {
                    'cdm_collection': 'Kathleen Gemberling Adkison Collection',
                    'dspace_out': 'k_gemberlilng',
                    'load': True
                },
                {
                    'cdm_collection': 'Ken Jacobson Photographs',
                    'dspace_out': 'ken_jacobson',
                    'load': True
                },
                {
                    'cdm_collection': 'Paulus Glass Plate Collection',
                    'dspace_out': 'paulus_glass_plate',
                    'load': True
                },
                {
                    'cdm_collection': 'Salem and Eastern Oregon Photographs',
                    'dspace_out': 'salem_and_eastern_oregon',
                    'load': True
                },
                {
                    'cdm_collection': 'Salem Eastern Oregon Photographs',
                    'dspace_out': 'salem_eastern_oregon',
                    'load': True
                },
                {
                    'cdm_collection': 'Sanders Soviet Poster Collection',
                    'dspace_out': 'soviet_poster',
                    'load': True
                },
                {
                    'cdm_collection': 'Vernor Martin Sackett Collection',
                    'dspace_out': 'sackett_photos',
                    'load': True
                },
                {
                    'cdm_collection': 'Willamette University Student Life Glass Negatives',
                    'dspace_out': 'student_life_glass_negatives',
                    'load': True
                },
                {
                    'cdm_collection': 'Willamette University Archives Chloe Clarke Willson Collection',
                    'dspace_out': '',
                    'load': False
                },
                {
                    'cdm_collection': 'Scrapbooks',
                    'dspace_out': '',
                    'load': False
                },
                {
                    'cdm_collection': 'Stowell Diary',
                    'dspace_out': '',
                    'load': False
                }
            ]
        }
    }
