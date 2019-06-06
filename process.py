#!/usr/bin/env python

import sys
from condm.controller import ContentdmController
from existdb.controller import ExistController

# Allowed repo names are 'cdm' and 'exist-db'.
#
# command line arguments
# process.py <repo> <collection> <source_file or directory> <outputdirectory>
#
# example1 ./process.py cdm manuscripts archives_manuscripts.xml archives_manuscripts
# example2 ./process.py exist collegian collegian collegian
#
# example1 uses a source file; example2 uses a source directory.
#
# NOTE: You must provide an empty output directory.  E.g. saf/archives_manuscripts.
#       This directory must be empty.
#
# See controller classes for more details.

# The source repository
repo = sys.argv[1]

if repo == 'cdm':
    controller = ContentdmController(sys.argv[2], sys.argv[3], sys.argv[4])
    controller.process_collections()

if repo == 'exist':
    controller = ExistController(sys.argv[2], sys.argv[3], sys.argv[4])
    controller.process_records()