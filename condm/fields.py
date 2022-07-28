

class Fields:
    """
    Use this class manages field names used by DSpace and CONTENTdm. (Do not use string values in the code.)
    """
    def __init__(self):
        pass

    # DC fields as they are exported by CONTENTdm. Includes "unmapped".
    cdm_dc_field = {
        'unmapped': 'unmapped',
        'title': 'title',
        'creator': 'creator',
        'alt_title': 'alternative',
        'subject': 'subject',
        'publisher': 'publisher',
        'contributor': 'contributor',
        'source': 'source',
        'accrual_method': 'accrualMethod',
        'accrual_policy': 'accrualPolicy',
        'accrual_periodicity': ' accrualPeriodicity',
        'instruction_method': 'instructional',
        'description': 'description',
        'description_table_of_contents': 'tableOfContents',
        'description_abstract': 'abstract',
        'date': 'date',
        'date_created': 'created',
        'date_valid': 'valid',
        'date_available': 'available',
        'date_issued': 'issued',
        'date_modified': 'modified',
        'date_accepted': 'accepted',
        'date_copyrighted': 'copyrighted',
        'date_submitted': 'submitted',
        'identifier': 'identifier',
        'identifier_bibliographic_citation': 'citation',
        'language': 'language',
        'format': 'format',
        'format_extent': 'extent',
        'format_medium': 'medium',
        'relation': 'relation',
        'relation_requires': 'requires',
        'relation_is_required_by': 'isRequiredBy',
        'relation_is_part_of': 'isPartOf',
        'relation_is_version_of': 'isVersionOf',
        'relation_is_replaced_by': 'isReplacedBy',
        'relation_replaces': 'replaces',
        'relation_has_version': 'hasVersion',
        'relation_is_referenced_by': 'isReferencedBy',
        'relation_references': 'references',
        'relation_is_format_of': 'isFormatOf',
        'relation_has_part': 'hasPart',
        'relation_has_format': 'hasFormat',
        'relation_conforms_to': 'conformsTo',
        'rights_access': 'access',
        'rights_license': 'license',
        'rights_holder': 'holder',
        'rights': 'rights',
        'coverage': 'coverage',
        'coverage_spatial': 'spatial',
        'coverage_temporal': 'temporal',
        'audience_mediator': 'mediator',
        'audience': 'audience',
        'audience_level': 'level',
        'provenance': 'provenance',
        'type': 'type'
    }

    # Non-dc (e.g. structural) xml elements exported by cdm.
    cdm_structural_elements = {
        'id': 'cdmid',
        'filename': 'cdmfile',
        'filepath': 'cdmpath',
        'date_created': 'cdmcreated',
        'thumbnail': 'thumbnailURL',
        'preservation_location': 'fullResolution',
        'compound_object_container': 'structure',
        'compound_object_page': 'page',
        'compound_object_page_pointer': 'pageptr',
        'compound_object_page_title': 'pagetitle',
        'compound_object_page_file': 'pagefile',
        'compound_object_page_file_type': 'pagefiletype',
        'compound_object_page_file_loc': 'pagefilelocation',
        'compound_object_page_text': 'pagetext',
        'compound_object_access_file': 'access',
        'compound_object_thumb_file': 'thumbnail'
    }

    # Fields used for DSpace dublin core import
    dspace_dc_field = {
        'title': 'title',
        'title_alt_qualifier': 'alternative',
        'creator': 'creator',
        'contributor': 'contributor',
        'contributor_author_qualifier': 'author',
        'description': 'description',
        'description_provenance_qualifier': 'provenance',
        'description_sponsorship_qualifier': 'sponsorship',
        'date': 'date',
        'date_created_qualifier': 'created',
        'date_issued_qualifier': 'issued',
        'subject': 'subject',
        'source': 'source',
        'relation': 'relation',
        'relation_uri_qualifier': 'uri',
        'relation_ispartof_qualifier': 'ispartof',
        'relation_isformatof_qualifier': 'isformatof',
        'relation_isreferencedby_qualifer': 'isreferencedby',
        'require_relation': 'requires',
        'coverage': 'coverage',
        'coverage_spatial_qualifier': 'spatial',
        'coverage_temporal_qualifier': 'temporal',
        'language': 'language',
        'language_iso_qualifier': 'iso',
        'identifier': 'identifier',
        'identifier_other_qualifier': 'other',
        'publisher': 'publisher',
        'type': 'type',
        'format': 'format',
        'format_medium_qualifier': 'medium',
        'format_extent_qualifier': 'extent',
        'rights': 'rights',
        'rights_uri_qualifier': 'uri'
    }

    # Fields for dspace local metadata import.
    dspace_local_field = {
        'eadid': 'EADID',
        'preservation_location': 'mastercopy',
        'mets_identifier': 'METSID',
        'transcription': 'transcription',
        'addressee': 'addressee',
        'postmark': 'postmark',
        'browse_date': 'browse',
        'personal_name': 'personalname',
        'location_gps': 'location',
        'date': 'date',
        'interviewer': 'interviewer',
        'interviewee': 'interviewee',
        'aat': 'aat',
        'order_number': 'ordernumber',
        'load_number': 'loadnumber',
        'culture': 'culture',
        'geo_name': 'geoname',
        'object_type': 'objecttype',
        'dependency': 'dependency'
    }

    # Art collection records have separate dimension fields rather than a single element.
    # This map is used to create a single format.extent field.
    format_extent_fields = {
        'accrualMethod': 'units',
        'accrualPeriodicity': 'depth',
        'accrualPolicy': 'height',
        'dateModified': 'width'
    }
