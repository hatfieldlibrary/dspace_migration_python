#!/usr/bin/env python

import urllib
import time
from fieldMap import FieldMaps


class FetchBitstreams:

    def __init__(self):
        pass

    @staticmethod
    def appendToContents(current_dir, filename, error_count, line):
        """
        Appends a new file name to the saf item contents file.
        :param current_dir: the current item saf directory.
        :param filename: the file name (string)
        :param error_count: the current error count
        :param line: either 1 or 0, with 0 representing the first line of the file (no preceding line break)
        :return: the error count
        """
        contents_out = current_dir + '/contents'

        try:
            content_file = open(contents_out, 'a')
            if line == 0:
                # first write to the contents file.
                content_file.write(filename)
            else:
                content_file.write('\n' + filename)
        except:
            error_count += 1
            print('An error occurred writing to %s for the record %s' % (contents_out, filename))

        content_file.close()
        return error_count


    @staticmethod
    def fetchThumbnail(outfile, link, doc_title, error_count):
        """
        Fetches the thumbnail file and writes to the saf item directory.
        :param outfile: full path for the file to be written.
        :param link: link used to retrieve the file from contentdm.
        :param doc_title: the title of the current document (for error logging).
        :param error_count: the current error count.
        :return: the error count.
        """
        if link is not None:

            try:
                urllib.urlretrieve(link, outfile)
            except IOError as err:
                print('An error occured retriveing thumbnail for: %s' % (doc_title))
                print('IO Error: {0}'.format(err))
            except:
                error_count += 1
                print('An error occurred retrieving thumbnail for: %s' % (doc_title))

            return error_count

    def fetchThumbnailOnly(self, current_dir, record, collection):
        """
        This function is used for compound objects. Compound objects do not download page bitstreams into
        dspace.  But a thumbnail image is still required.
        :param current_dir: the full path to the saf output directory
        :param record: the etree element for a contentdm record
        :param collection: the contentdm collection name
        """
        fields = FieldMaps()
        cdm = fields.getCdmFieldMap()
        error_count = 0
        cdmid = record.find(cdm['id'])
        cdmfile = record.find(cdm['filename'])
        doc_title = record.find(cdm['title'])
        thumbnail_url = record.find(cdm['thumbnail'])
        # the jpg file name; this assumes a cpd (compound object) file. Will break for other file types.
        thumbname = cdmfile.text.replace('cpd', 'jpg')
        # the thumbnail output file
        outfile = current_dir + '/' + thumbname
        # thumbnail link
        link = FetchBitstreams.createThumbnailLink(collection, cdmid.text)

        if thumbnail_url.text is not None:
            error_count = FetchBitstreams.fetchThumbnail(outfile, link, doc_title.text, error_count)
            error_count = FetchBitstreams.appendToContents(current_dir, thumbname, error_count, 1)

            if error_count > 0:
                print('%s --  Thumbnail %s proccessed with %s errors.' % (doc_title.text, thumbname, error_count))


    @staticmethod
    def fetchBitstream(outfile, link, doc_title, error_count):
        """
        Fetches single bitstream and writes to saf directory
        :param outfile: the file name and output path for the bitstream
        :param link: the url to retrieve the bitstream
        :param doc_title: the title of the current document (dc)
        :param error_count: the current error count
            :return: the error count, incremented if an error encountered
        """
        try:
            urllib.urlretrieve(link, outfile)
        except IOError as err:
            print('An error occured retriveing bitstreams for: %s' % (doc_title))
            print('IO Error: {0}'.format(err))
        except:
            error_count += 1
            print('An error occurred retrieving bitstreams for: %s' % (doc_title))

        return error_count

    @staticmethod
    def createThumbnailLink(collection, cdmid):
        return 'http://condm.willamette.edu:81/cgi-bin/thumbnail.exe?CISOROOT=/' + collection + '&CISOPTR=' + cdmid

    @staticmethod
    def createBitstreamLink(collection, cdmid):
        return 'http://condm.willamette.edu:81/cgi-bin/showfile.exe?CISOROOT=/' + collection + '&CISOPTR=' + cdmid


    def fetchBitStreams(self, current_dir, record, collection):
        """
        Extract the bitstream url from metadata, fetch the bitstream, and add to simple archive format entry.
        If a thumbnail image url is available, repeat operation for the thumbnail. This function throws and error
        if called for a compound object.
        :param current_dir: the full path to the saf output directory
        :param record: the etree element for a contentdm record
        :param collection: the contentdm collection name
        """
        fields = FieldMaps()
        map = fields.getCdmFieldMap()
        cdmid_el = record.find(map['id'])

        if cdmid_el is None:
            print('Error: no cdmid found')

        else:
            if cdmid_el is not None:

                error_count = 0
                doc_title_el = record.find(map['title'])
                cdmfile_el = record.find(map['filename'])
                thumb_url_el = record.find(map['thumbnail'])

                # cdm link for bitstream
                link = FetchBitstreams.createBitstreamLink(collection, cdmid_el.text)

                # the output filename for the bitstream.
                outfile = current_dir + '/' + cdmfile_el.text
                error_count = FetchBitstreams.fetchBitstream(outfile, link, doc_title_el.text, error_count)

                error_count = FetchBitstreams.appendToContents(current_dir, cdmfile_el.text, error_count, 0)

                # check for thumbnail url in the cdm record.
                if thumb_url_el.text is not None:
                    # the jpg file name; this assumes a jp2 file or pdf file. Will break for other file types.
                    thumbname = cdmfile_el.text.replace('jp2', 'jpg').replace('pdf', 'jpg')

                    # defines the output location for the thumbnail .jpg
                    outfile = current_dir + '/' + thumbname

                    # cdm link for thumbnail
                    link = FetchBitstreams.createThumbnailLink(collection, cdmid_el.text)

                    error_count = FetchBitstreams.fetchThumbnail(outfile, link, doc_title_el.text, error_count)
                    error_count = FetchBitstreams.appendToContents(current_dir, thumbname, error_count, 1)

                    if error_count > 0:
                        print('%s --  Thumbnail %s proccessed with %s errors.' %
                              (doc_title_el.text, thumbname, error_count))

                # being nice, but this also works running full speed ahead.
                time.sleep(.200)

                if cdmfile_el.text.find('cpd') != -1:
                    raise RuntimeError('ERROR: Requesting bitstreams for a compound object.')
                # else:
                    # print('%s --  Bitstream %s retrieved with %s errors.' %
                    #      (doc_title_el.text, cdmfile_el.text, error_count))
