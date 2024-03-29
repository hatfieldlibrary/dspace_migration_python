#!/usr/bin/env python

import sys
import argparse
from condm.controller import ContentdmProcessor
from existdb.controller import ExistProcessor

# Allowed repo names are 'cdm' and 'exist-db'.
#
# command line arguments
# process.py <repo> <collection> <source_file or directory> <outputdirectory>
#
# example1 ./process.py cdm manuscripts archives_manuscripts.xml archives_manuscripts --dry-run
# example2 ./process.py exist collegian collegian collegian
#
# example1 uses a source file; example2 uses a source directory.
#
# NOTE: You must provide an empty output directory.  E.g. saf/archives_manuscripts.
#       This directory must be empty.
#
# See processor classes for more details.

# The source repository

parser = argparse.ArgumentParser(description='Process exported collection data to saf. The supported repositories are CONTENTdm and the WU eXist-db METS/ALTO collections.')
parser.add_argument('repo', metavar='repo', type=str,
                    help='the repository name (cdm | exist)')
parser.add_argument('collection', metavar='collection', type=str,
                    help='the repository collection name')
parser.add_argument('source_file', metavar='source_file', type=str,
                    help='the exported xml data source')
parser.add_argument('saf_dir', metavar='saf_directory', type=str,
                    help='the parent saf target directory')
parser.add_argument("-d", "--dry-run", action="store_true",
                    help="Dry run displays collection analytics only. No data is processed.")
args = parser.parse_args()

repo = args.repo

dry_run = False
if args.dry_run:
    dry_run = True

if repo == 'cdm':
    controller = ContentdmProcessor(args.collection, args.source_file, args.saf_dir, dry_run)
    controller.process_collections()

if repo == 'exist':
    controller = ExistProcessor(args.collection, args.source_file, args.saf_dir, dry_run)
    controller.process_records()
