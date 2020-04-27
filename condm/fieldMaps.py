
from .fields import Fields


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

    # Maps cdm fields to dspace dublin core fields.

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
            'element': dspace_dc_field['contributor'],
            'qualifier': dspace_dc_field['contributor_author_qualifier']
        },
        cdm_dc_field['contributor']: {
            'element': dspace_dc_field['contributor'],
            'qualifier': dspace_dc_field['contributor_author_qualifier']
        },
        cdm_dc_field['description']: {
            'element': dspace_dc_field['description'],
            'qualifier': None
        },
        # Dspace creates it's own description.provenance at import.
        cdm_dc_field['provenance']: {
            'element': dspace_dc_field['description'],
            'qualifier': dspace_dc_field['description_provenance_qualifier']
        },
        cdm_dc_field['relation_is_referenced_by']: {
            'element': dspace_dc_field['description'],
            'qualifier': dspace_dc_field['description_sponsorship_qualifier']
        },
        cdm_dc_field['date']: {
            'element': dspace_dc_field['date'],
            'qualifier': dspace_dc_field['date_created_qualifier']
        },
        cdm_dc_field['coverage_spatial']: {
            'element': dspace_dc_field['coverage'],
            'qualifier': dspace_dc_field['coverage_spatial_qualifier']
        },
        cdm_dc_field['coverage_temporal']: {
            'element': dspace_dc_field['coverage'],
            'qualifier': dspace_dc_field['coverage_temporal_qualifier']
        },
        cdm_dc_field['subject']: {
            'element': dspace_dc_field['subject'],
            'qualifier': None
        },
        cdm_dc_field['relation']: {
            'element': dspace_dc_field['relation'],
            'qualifier': dspace_dc_field['relation_isreferencedby_qualifer']
        },
        cdm_dc_field['relation_is_part_of']: {
            'element': dspace_dc_field['relation'],
            'qualifier': dspace_dc_field['relation_ispartof_qualifier']
        },
        cdm_dc_field['relation_is_format_of']: {
            'element': dspace_dc_field['relation'],
            'qualifier': dspace_dc_field['relation_isformatof_qualifier']
        },
        cdm_dc_field['language']: {
            'element': dspace_dc_field['language'],
            'qualifier': dspace_dc_field['language_iso_qualifier']
        },
        cdm_dc_field['identifier']: {
            'element': dspace_dc_field['identifier'],
            'qualifier': dspace_dc_field['identifier_other_qualifier']
        },
        # This is the doi field.
        cdm_dc_field['instruction_method']: {
            'element': dspace_dc_field['identifier'],
            'qualifier': None
        },
        cdm_dc_field['publisher']: {
            'element': dspace_dc_field['publisher'],
            'qualifier': None
        },
        cdm_dc_field['rights_license']: {
            'element': dspace_dc_field['rights'],
            'qualifier': None
        },
        cdm_dc_field['rights']: {
            'element': dspace_dc_field['rights'],
            'qualifier': dspace_dc_field['rights_uri_qualifier']
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

    # Maps cdm fields to dspace local metadata fields.

    local_field_map = {

        cdm_structural_elements['preservation_location']: {
            'element': dspace_local_field['preservation_location'],
            'qualifier': None
        },
        cdm_dc_field['relation_is_required_by']: {
            'element': dspace_local_field['eadid'],
            'qualifier': None
        },
        # We also create a local field for a unique contentdm record identifier.
        # This record is generated by combining the collection name and the contentdm pointer.
        dspace_local_field['mets_identifier']: {
            'element': dspace_local_field['mets_identifier'],
            'qualifier': None
        },
        cdm_dc_field['identifier_bibliographic_citation']: {
            'element': dspace_local_field['transcription'],
            'qualifier': None
        },
        cdm_dc_field['description_table_of_contents']: {
            'element': dspace_local_field['addressee'],
            'qualifier': None
        },
        cdm_dc_field['date_issued']: {
            'element': dspace_local_field['postmark'],
            'qualifier': None
        },
        cdm_dc_field['date_valid']: {
            'element': dspace_local_field['browse_date'],
            'qualifier': None
        },
        cdm_dc_field['date_created']: {
            'element': dspace_local_field['date'],
            'qualifier': None
        },
        cdm_dc_field['audience_mediator']: {
            'element': dspace_local_field['personal_name'],
            'qualifier': None
        },
        cdm_dc_field['coverage']: {
            'element': dspace_local_field['location_gps'],
            'qualifier': None
        },
        cdm_dc_field['date_submitted']: {
            'element': dspace_local_field['interviewer'],
            'qualifier': None
        },
        cdm_dc_field['date_copyrighted']: {
            'element': dspace_local_field['interviewee'],
            'qualifier': None
        },
        cdm_dc_field['relation_conforms_to']: {
            'element': dspace_local_field['aat'],
            'qualifier': None
        },
        cdm_dc_field['relation_references']: {
            'element': dspace_local_field['order_number'],
            'qualifier': None
        },
        cdm_dc_field['relation_has_part']: {
            'element': dspace_local_field['load_number'],
            'qualifier': None
        },
        cdm_dc_field['audience']: {
            'element': dspace_local_field['culture'],
            'qualifier': None
        },
        cdm_dc_field['audience_level']: {
            'element': dspace_local_field['geo_name'],
            'qualifier': None
        }
    }
