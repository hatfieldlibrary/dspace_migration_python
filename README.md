# Simple Archive Format Processing

We plan to use the DSpace Simple Archive Format (saf) to import data from CONTENTdm and eXist-db into DSpace.

The initial commit fully implements exporting from CONTENTdm with the following caveats:

1. Data was exported as "CONTENTdm Standard XML" with the "include only the full text field from page-level metadata"
option.
2. Metadata mapping between systems is incomplete and will change with more analysis.
3. The local DSpace metadata fields assigned to administrative and application-specific metadata are provisional.
4. We have not considered workflow details for during and after the migration period.

For **saf** documentation, see https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format

## Code Usage and Status

A top-level process.py script takes command line arguments.  See the script for documentation.

All subsequent work is done by python classes that have been coded separately for CONTENTdm and eXist-db repositories
(work on the latter is incomplete).

Output is written to **saf** sub-directories, each containing up to 1000 items. Data in **saf** subdirectories has been
 imported into DSpace.  Records include images, PDF, and compound objects, each with thumbnails and 
administrative metadata. To date, approximately 7000 items have been loaded.

Our data import tests are currently done with DSpace 6.  Our target repository will be DSpace 7.  We do not anticipate changes
in the DSpace import interface between versions 6 and 7.