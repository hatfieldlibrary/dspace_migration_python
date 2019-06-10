# Simple Archive Format Processing

We plan to use the DSpace Simple Archive Format (saf) to import data from CONTENTdm and eXist-db into DSpace.

For **saf** documentation, see https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format

## Code Usage 
```
usage: process.py [-h] [-d] repo collection source_file saf_directory

Process contentdm exported collection to saf.

positional arguments:
  repo           the repository name (cdm | exist)
  collection     the repository collection name
  source_file    the exported xml data source
  saf_directory  the parent saf target directory

optional arguments:
  -h, --help     show this help message and exit
  -d, --dry-run  Dry run displays collection analytics only. No data is
                 processed.
```
You need to create "data" and "saf" directories for CONTENTdm and eXist-db.  For example, `./existdb/data` and `./existdb.saf`.

The input data files from CONTENTdm and eXist-db go into the data directories. Output will be written to `saf` sub-directories.


## Metadata

### CONTENTdm
For CONTENTdm, two classes control the program output.  `CollectionConfig` contains dictionaries that define how
CONTENTdm collection fields (e.g. as defined in the Dublin Core source field) will be processed.  The `FieldMap`
class contains mapping between CONTENTdm record and DSpace Dublic Core and Local DSpace fields.

### Existdb
Extracting metadata from mets is slightly more complex. Data is extracted based on elements, attributes and attribute
values that are defined in the `ExistDbFields` class. The mods metadata can be sparse, so a few default values are 
defined in the `DefaultFieldValueMap` class. All exported records will include these default values if they are not
provided in the mets.

## Analytics
Running the program with the `--dry-run` flag will produce a brief analytics report (without loading any data).

Here is a sample:
```$xslt
 
SUB-COLLECTIONS
 
Item counts for sub-collections
 800: Vernor Martin Sackett Collection
  70: Sanders Soviet Poster Collection
  18: Willamette University Student Life Glass Negatives
   1: Stowell Diary
  78: Kathleen Gemberling Adkison Collection
2700: Campus Photographs
  29: Helen Pearce Collection
  42: Ken Jacobson Photographs
 161: Postcard Collection
  38: Salem Eastern Oregon Photographs
1363: Paulus Glass Plate Collection
   1: Willamette University Archives Chloe Clarke Willson Collection
 
Item counts for all unprocessed collections (these will be added to the "base" saf directory).
  1: Scrapbooks
  1: Salem and  Eastern Oregon Photographs;
  1:       PNAA
 12: Willamette University Archives Paulus Glass Plate Collection
  1: Scrapbooks;
 
Item counts for collections that were excluded by configuration.
  1: Scrapbooks
  1:       PNAA
  1: Scrapbooks;
 
ITEM TYPES
   2: Compound Objects
 120: Items with multiple bitstreams
5195: Single bitstream items
 
5317 records processed in dry run of aphotos
```  
