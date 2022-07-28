
class CollectionConfig:

    # This class is for collection level configuration.

    def __init__(self):
        pass

    # Defines sub-collections that include compound objects that should be loaded
    # into dspace as single records, with more than one bitstream (e.g. the Postcard Collection).
    # Use the field_values array to define sub-collections. If no sub-collections exist
    # you can specify the 'allSubCollections' field_name (e.g. the art collection contains
    # no sub-collections).  To force compound objects to be processed as documents just
    # provide a normal field_name with an empty field_values array.
    collections_to_omit_compound_objects = {
        'aphotos': {
            'field_name': 'source',
            'field_values': [
                'Postcard Collection',
                'Kathleen Gemberling Adkison Collection',
                'Ken Jacobson Photographs'
            ]
        },
        'manuscripts': {
            'field_name': 'source',
            'field_values': []
        },
        'pnaa': {
            'field_name': 'source',
            'field_values': [
                'Kathleen Gemberling Adkison Collection',
                'Henk Pander papers',
                'Jim Shull Works by Northwest Artists Slide Collection; Pacific Northwest Artists Archive'
            ]
        },
        'glee': {
            'field_name': 'source',
            'field_values': []
        },
        'rare': {
            'field_name': 'source',
            'field_values': []
        },
        'hfmanw': {
            'field_name': 'source',
            'field_values': []
        },
        'hfmoaevents': {
            'field_name': 'source',
            'field_values': []
        },
        'aoc': {
            'field_name': 'allSubCollections',
            'field_values': []
        }
    }

    # Maps contentdm collection names to saf directories.
    # If the load value is False, the collection will not
    # be processed to an saf directory for that collection.
    # Instead, it will be processed into the "base" saf
    # directory so its metadata can be reviewed.
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
                    'cdm_collection': 'Paulus Glass Plate Collection',
                    'dspace_out': 'paulus_glass_plate',
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
                    'dspace_out': 'chloe_willson',
                    'load': True
                },
                {
                    'cdm_collection': 'Stowell Diary',
                    'dspace_out': 'stowell_image',
                    'load': True
                },
                {
                    'cdm_collection': 'Scrapbooks',
                    'dspace_out': '',
                    'load': False
                },
                {
                    'cdm_collection': 'Scrapbooks;',
                    'dspace_out': '',
                    'load': False
                },
                {
                    'cdm_collection': '      PNAA',
                    'dspace_out': '',
                    'load': False
                }
            ]
        },
        'manuscripts': {
            'field_name': 'source',
            'field_values': [
                {
                    'cdm_collection': 'Charles E. Larsen Chemawa Indian School Collection',
                    'dspace_out': 'charles_larsen',
                    'load': True
                },
                {
                    'cdm_collection': 'Chloe Clarke Willson Collection',
                    'dspace_out': 'chloe_clarke_willson',
                    'load': True
                },
                {
                    'cdm_collection': 'James H. Wilbur Letters',
                    'dspace_out': 'james_wilbur',
                    'load': True
                },
                {
                    'cdm_collection': 'John G. Burggraf Letters',
                    'dspace_out': 'john_burggraf',
                    'load': True
                },
                {
                    'cdm_collection': 'Office of the President: Francis S. Hoyt letter',
                    'dspace_out': 'frances_hoyt',
                    'load': True
                },
                {
                    'cdm_collection': 'Office of the President: Nelson Rounds papers',
                    'dspace_out': 'nelson_rounds',
                    'load': True
                },
                {
                    'cdm_collection': 'Stowell Diary',
                    'dspace_out': 'stowell_diary',
                    'load': True
                },
                {
                    'cdm_collection': 'The John D. Beach Civil War Letters Collection',
                    'dspace_out': 'john_beach',
                    'load': True
                },
                {
                    'cdm_collection': 'The Waltz family papers',
                    'dspace_out': 'waltz_family',
                    'load': True
                },
                {
                    'cdm_collection': 'Viola Price Franklin Letter Collection',
                    'dspace_out': 'viola_price',
                    'load': True
                },
                {
                    'cdm_collection': 'Constance Fowler Collection',
                    'dspace_out': 'constance_fowler',
                    'load': True
                },
                {
                    'cdm_collection': 'Robert W. "Bob" Packwood papers',
                    'dspace_out': 'bob_packwood',
                    'load': True
                },
            ]
        },
        'glee': {
            'field_name': 'source',
            'field_values': []
        },
        'pnaa': {
            'field_name': 'source',
            'field_values': [
                {
                    'cdm_collection': 'Jim Shull Works by Northwest Artists Slide Collection; Pacific Northwest Artists Archive',
                    'dspace_out': 'shull_slide_collection',
                    'load': True
                },
                {
                    'cdm_collection': 'Kathleen Gemberling Adkison Collection',
                    'dspace_out': 'k_gemberlilng',
                    'load': True
                },
                {
                    'cdm_collection': 'Jim Shull Works by Northwest Artists Slide Collection',
                    'dspace_out': 'j_shull',
                    'load': True
                },
                {
                    'cdm_collection': 'Nelson and Olive Sandgren Collection',
                    'dspace_out': 'n_o_sandgren',
                    'load': True
                },
                {
                    'cdm_collection': 'Stella Douglas papers',
                    'dspace_out': 's_douglas',
                    'load': True
                },
                {
                    'cdm_collection': 'Tom Hardy papers',
                    'dspace_out': 't_hardy',
                    'load': True
                },
                {
                    'cdm_collection': 'Tom Cramer papers',
                    'dspace_out': 't_cramer',
                    'load': True
                },
                {
                    'cdm_collection': 'Nicholsloy Studio Collection',
                    'dspace_out': 'nicholsloy',
                    'load': True
                },
                {
                    'cdm_collection': 'Henk Pander papers',
                    'dspace_out': 'h_pander',
                    'load': True
                },
                {
                    'cdm_collection': 'Myra Wiggins Papers',
                    'dspace_out': 'm_wiggins',
                    'load': True
                },
                {
                    'cdm_collection': 'Judith and Jan Zach papers',
                    'dspace_out': 'j_j_zach',
                    'load': True
                },
                {
                    'cdm_collection': 'Ken Jacobson Photographs',
                    'dspace_out': 'ken_jacobson',
                    'load': True
                },
                {
                    'cdm_collection': 'Kathleen Gemberling Adkison Collection; Pacific Northwest Artists Archive',
                    'dspace_out': 'k_gemberlilng-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Nelson and Olive Sandgren Collection; Pacific Northwest Artists Archive',
                    'dspace_out': 'n_o_sandgren-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Stella Douglas papers; Pacific Northwest Artists Archive',
                    'dspace_out': 's_douglas-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Tom Hardy papers; Pacific Northwest Artists Archive',
                    'dspace_out': 't_hardy-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Tom Cramer papers; Pacific Northwest Artists Archive',
                    'dspace_out': 't_cramer-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Nicholsloy Studio Collection; Pacific Northwest Artists Archive',
                    'dspace_out': 'nicholsloy-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Henk Pander papers; Pacific Northwest Artists Archive',
                    'dspace_out': 'h_pander-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Myra Wiggins Papers; Pacific Northwest Artists Archive',
                    'dspace_out': 'm_wiggins-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Judith and Jan Zach papers; Pacific Northwest Artists Archive',
                    'dspace_out': 'j_j_zach-2',
                    'load': True
                },
                {
                    'cdm_collection': 'Ken Jacobson Photographs; Pacific Northwest Artists Archive',
                    'dspace_out': 'ken_jacobson-2',
                    'load': True
                }
                # {
                #     'cdm_collection': 'PNAA',
                #     'dspace_out': '',
                #     'load': True
                # },
                # {
                #     'cdm_collection': 'Pacific Northwest Artists Archive',
                #     'dspace_out': '',
                #     'load': True
                # },
            ]
        },
        'rare': {
            'field_name': 'source',
            'field_values': []
        },
        'hfmanw': {
            'field_name': 'source',
            'field_values': [
                 {
                    'cdm_collection': 'Native American Collection',
                    'dspace_out': 'native_am',
                    'load': True
                },
                {
                    'cdm_collection': 'Crow\'s Shadow Institute of the Arts',
                    'dspace_out': 'crows',
                    'load': True
                },
                {
                    'cdm_collection': 'Northwest Art Collection',
                    'dspace_out': 'northwest',
                    'load': True
                },
                {
                    'cdm_collection': 'Survey Collection',
                    'dspace_out': 'survey',
                    'load': True
                }, 
                {
                    'cdm_collection': 'Ancient Art Collection',
                    'dspace_out': 'ancient',
                    'load': True
                },
                {
                    'cdm_collection': 'European Art Collection',
                    'dspace_out': 'europe',
                    'load': True
                },
{
                    'cdm_collection': 'Asian Art Collection',
                    'dspace_out': 'asian',
                    'load': True
                },
{
                    'cdm_collection': 'American Art Collection',
                    'dspace_out': 'american',
                    'load': True
                },
                ]
        },
        'hfmoaevents': {
            'field_name': 'source',
            'field_values': []
        },
        'aoc': {
            'field_name': 'source',
            'field_values': []
        }

    }

