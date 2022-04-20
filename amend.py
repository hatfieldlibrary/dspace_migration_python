from add_iiif_meta.add_metadata import AddMetadata
import argparse

parser = argparse.ArgumentParser(description='Amends SAf directory by adding dspace nd iiif metadata files.')


parser.add_argument('-a', '--amend', action='store_true',
                    help='Adds missing metadata to items')
parser.add_argument('metadata_saf_dir', metavar='metadata_saf_dir', type=str,
                    help='The directory to amend with missing metadata')

args = parser.parse_args()

if args.amend:
    controller = AddMetadata(args.metadata_saf_dir)
    controller.add_metadata()
