from add_iiif_meta.add_metadata import AddMetadata
from thumb_update.update_thumbs import UpdateThumbs
import argparse

parser = argparse.ArgumentParser(description='Amends SAf directories.')


parser.add_argument('-m', '--meta', action='store_true',
                    help='Adds missing metadata to items')
parser.add_argument('-t', '--thumb', action='store_true',
                    help='Replaces thumbnail images')
parser.add_argument('repo', metavar='repo', type=str,
                    help='The repository (condm|existdb)')
parser.add_argument('saf_dir', metavar='saf_dir', type=str,
                    help='The directory to amend')
parser.add_argument('batch_name', metavar='batch_name', type=str,
                    help='The batch directory name')
args = parser.parse_args()

if args.meta:
    controller = AddMetadata(args.saf_dir, args.repo)
    controller.add_metadata()

if args.thumb:
    controller = UpdateThumbs(args.saf_dir, args.repo, args.batch_name)
    controller.update_thumbs()
