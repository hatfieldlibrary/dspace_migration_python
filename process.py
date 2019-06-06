#!/usr/bin/env python

import sys
import argparse
from condm.controller import ContentdmController
from existdb.controller import ExistController

# Allowed repo names are 'cdm' and 'exist-db'.
#
# command line arguments
# process.py <repo> <collection> <source_file or directory> <outputdirectory>
#
# example1 ./process.py cdm manuscripts archives_manuscripts.xml archives_manuscripts dry_run
# example2 ./process.py exist collegian collegian collegian
#
# example1 uses a source file; example2 uses a source directory.
#
# NOTE: You must provide an empty output directory.  E.g. saf/archives_manuscripts.
#       This directory must be empty.
#
# See controller classes for more details.

# The source repository

parser = argparse.ArgumentParser(description='Process contentdm exported collection to saf.')
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
    controller = ContentdmController(args.collection, args.source_file, args.saf_dir, dry_run)
    controller.process_collections()

if repo == 'exist':
    controller = ExistController(args.collection, args.source_file, args.saf_dir)
    controller.process_records()
