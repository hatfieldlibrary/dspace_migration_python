# Simple Archive Format Processing

This program generates DSpace Simple Archive Format (SAF) directories from data exported from
CONTENTdm and our local eXist-db METS/ALTO collections.

For DSpace **SAF** documentation, see https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format

## Code Usage 
```
usage: process.py [-h] [-d] repo collection source_file saf_directory

Process exported collection data to saf. The supported repositories are
CONTENTdm and the WU eXist-db METS/ALTO collections.

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
You need to create "data" and "saf" directories for CONTENTdm and eXist-db.  For example, `./existdb/data` and `./existdb/saf`.

The input xml files from CONTENTdm and eXist-db go into the corresponding `data` directories. 

Output will be written to `saf` subdirectories. You need to manually create the top-level `saf` directories for your
exported collections.  For example, `./condm/saf/photographs`.

## Export
Data must be exported from CONTENTdm as CONTENTdm Standard XML, including only the full-text field from page-level metadata.

For eXist-db METS/ALTO collections, the METS and full text collections are required for each publication.

## Metadata

### CONTENTdm
For CONTENTdm, two classes configure the program output: 
* `CollectionConfig` contains dictionaries that define how parent CONTENTdm collections will be sorted into smaller collections based on item metadata (e.g. as specified in the Dublin Core source field).  
* The `FieldMap` class contains mapping between the CONTENTdm record and DSpace Dublin Core and Local metadata fields.

### Existdb
Extracting metadata from METS is slightly more complex. Data extraction is based on elements, attributes and attribute
values that are defined in the `ExistDbFields` class. The MODS metadata can be sparse, so a few default values are 
defined in the `DefaultFieldValueMap` class. All exported records will include these default values if they are not
provided in the METS.

## Analytics
Running the program with the `--dry-run` flag will produce a brief analytics report (without loading any data). Currently enabled for CONTENTdm only.

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


## Simple Archive Format (SAF) Output

### CONTENTdm Collections
For CONTENTdm, each parent SAF directory contains subdirectories as defined in the `CollectionConfig`. (This step is
not required for eXist-db.) For CONTENTdm, the `CollectionConfig` can also be used to exclude specific
collections from compound object processing.

### SAF Directory Contents
Each SAF subdirectory contains numbered `batch` subdirectories. Each of these subdirectories contains up to 1000 items.

In each item directory, bitstream files may include images (jp2), thumbnail images, PDF files. The item directory may also include
a text file with transcriptions of CONTENTdm compound objects or eXist-db full text files.
 
The `contents` file in each item directory provides an inventory of the bitstream files.  The `dublin_core.xml` file contains all CONTENTdm Dublin
Core metadata mapped to DSpace fields (see `FieldMaps`).  The `metadata_local` file maps to our local DSpace
metadata registry (also configured in `FieldMaps`).

## DSpace Import
Items can be loaded into DSpace collections as show here:
https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format#ImportingandExportingItemsviaSimpleArchiveFormat-ImportingItems

