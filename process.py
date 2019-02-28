#!/usr/bin/env python

import sys
from condm.controller import ContentdmController

# Allowed repo names are 'cdm' and 'exist-db'.
#
# command line arguments
# controller.py <repo> <collection> <sourcefile> <outputdirectory>
#
# example ./process.py cdm manuscripts archives_manuscripts.xml archives_manuscripts
#
# See controller classes for more details.

# The source repository
repo = sys.argv[1]

if repo == 'cdm':
    controller = ContentdmController(sys.argv[2], sys.argv[3], sys.argv[4])
    controller.process_records()
