from urllib.request import urlretrieve
import time
from xml.etree.ElementTree import Element
from wand.image import Image

from .fields import Fields


class FetchBitstreams:
    cdm_dc = Fields.cdm_dc_field
    cdm_struc = Fields.cdm_structural_elements

    def __init__(self):
        pass

        # initialize info dict
        self.info = {
            "globalDefaults": {
                "activated": False,
                "label": "",
                "width": 0,
                "height": 0
            },
            "canvases": [],
            "structures": []
        }

    @staticmethod
    def append_to_contents(current_dir, filename, file_type):
        # type: (str, str, str) -> None
        """
        Appends a new file name to the saf item contents file.
        :param current_dir: the current item saf directory.
        :param filename: the file name (string)
        :param line: either 1 or 0, with 0 representing the first line of the file (no preceding line break)
        """
        contents_out = current_dir + '/contents'
        content_file = open(contents_out, 'a')
        if file_type == 'fulltext':
            # this is the first write to the contents file.
            content_file.write(filename + '\n')
            content_file.close()
        elif file_type == 'image':
            content_file.write(filename + '\tbundle:IIIF\n')
            content_file.close()
        elif file_type == 'thumbnail':
            content_file.write(filename + '\tbundle:THUMBNAIL\n')
            content_file.close()

    @staticmethod
    def __fetch_bitstream(outfile, link):
        # type: (str, str) -> None
        """
        Fetches single bitstream and writes to saf directory.
        Note that bitstream file names need not be unique in dspace
        because DSpace 6.x stores the name of a bitstream in the "dc.title" metadata field attached to the bitstream.
        However, they probably will be unique in all cases when in our contentdm
        exports, since the file name is derived from the exported xml.
        :param outfile: the file name and output path for the bitstream
        :param link: the url to retrieve the bitstream
        :param doc_title: the title of the current document (dc)
        :param error_count: the current error count
        :return: the error count, incremented if an error encountered
        """
        if link is not None:
            urlretrieve(link, outfile)

    @staticmethod
    def __create_thumbnail_link(collection, cdmid):
        # type: (str, str) -> str
        return 'http://condm.willamette.edu:81/cgi-bin/thumbnail.exe?CISOROOT=/' + collection + '&CISOPTR=' + cdmid

    @staticmethod
    def __create_bitstream_link(collection, cdmid):
        # type: (str, str) -> str
        return 'http://condm.willamette.edu:81/cgi-bin/showfile.exe?CISOROOT=/' + collection + '&CISOPTR=' + cdmid

    # @staticmethod
    # def fetch_thumbnail_only(current_dir, record, collection):
    #     # type: (str, Element, str) -> None
    #     """
    #     This function is used for compound objects. Compound objects do not import page bitstreams into
    #     dspace, but the import still wants to have thumbnail image.
    #     :param current_dir: the full path to the saf output directory
    #     :param record: the etree element for a contentdm record
    #     :param collection: the contentdm collection name
    #     """
    #     cdm_dc = Fields.cdm_dc_field
    #     cdm_struc = Fields.cdm_structural_elements
    #     cdmid = record.find(cdm_struc['id'])
    #     cdmfile = record.find(cdm_struc['filename'])
    #     doc_title = record.find(cdm_dc['title'])
    #     thumbnail_url = record.find(cdm_struc['thumbnail'])
    #     # the jpg file name; this assumes a cpd (compound object) file. Will break for other file types.
    #     thumbname = cdmfile.text.replace('cpd', 'jpg')
    #     # the thumbnail output file
    #     outfile = current_dir + '/' + thumbname
    #     # thumbnail link
    #     link = FetchBitstreams.__create_thumbnail_link(collection, cdmid.text)
    #     if thumbnail_url.text is not None:
    #         FetchBitstreams.__fetch_bitstream(outfile, link)
    #         FetchBitstreams.append_to_contents(current_dir, thumbname, 'thumbnail')

    @staticmethod
    def add_image_bitstream(cdmid_el, cdmfile, current_dir, collection, page_count):
        # type (Element, str, str, str, int) -> None
        """
        Adds a bitstream to the saf directory
        :param cdmid_el: the Element containing the contentdm pointer text
        :param cdmfile: the element containing the cdmfile text
        :param current_dir: the output directory
        :param collection: the contentdm collection
        :param page_count: indicates when to add line break to the contents file
        :return:
        """
        link = FetchBitstreams.__create_bitstream_link(collection, cdmid_el.text)
        # the output filename for the bitstream.
        outfile = current_dir + '/' + cdmfile
        FetchBitstreams.__fetch_bitstream(outfile, link)
        print('writing contents to ' + current_dir)
        FetchBitstreams.append_to_contents(current_dir, cdmfile, 'image')

    @staticmethod
    def create_thumbnail(current_dir, cdm_file):
        try:
            with Image(filename=current_dir + '/' + cdm_file) as f:
                f.format = 'jpeg'
                f.save(filename='temp.jpg')
        except Exception as err:
            print('An error occurred when creating temp file: %s' % err)
        try:
            with Image(filename='temp.jpg') as f:
                ratio = float(f.width) / float(f.height)
                height = f.height
                width = f.width

                if height > width:
                    if height > 175:
                        height = 175
                        width = int(175.0 * ratio)
                else:
                    if width > 175:
                        width = 175
                        height = int(175.0 / ratio)

                f.resize(width, height)
                f.save(filename=current_dir + '/thumb.jpg.jpg')
                FetchBitstreams.append_to_contents(current_dir, 'thumb.jpg.jpg', 'thumbnail')
        except Exception as err:
            print('An error occurred converting image for: %s.' % current_dir)
            print(err)

    # @staticmethod
    # def add_thumbnail(cdmid, cdm_file, thumb, current_dir, collection, page_count):
    #     # type (str, str, str, str, str, int) -> None
    #     """
    #     Adds a thumbnail image to the saf directory
    #     :param cdmid: the contentdm pointer
    #     :param cdm_file: the file name of contentdm bitstream
    #     :param thumb: file name of the thumbnail image
    #     :param current_dir: the output directory
    #     :param collection: the contentdm collection name
    #     :param page_count: indicates when to add line break to the contents file
    #     :return:
    #     """
    #     # Always pass a thumb object with type other than None if a thumbnail exists.
    #     if thumb is not None:
    #         thumbname = cdm_file.replace('jp2', 'jpg').replace('pdf', 'jpg')
    #         # defines the output location for the thumbnail .jpg
    #         outfile = current_dir + '/' + thumbname
    #          # cdm link for thumbnail
    #         link = FetchBitstreams.__create_thumbnail_link(collection, cdmid)
    #         FetchBitstreams.__fetch_bitstream(outfile, link)
    #         FetchBitstreams.append_to_contents(current_dir, thumbname, 'thumbnail')

    @staticmethod
    def fetch_multiple_bitsteams(cdmid_el, current_dir, record, collection):
        # type (Element, str, str, str) -> None
        """
        This function is used to request multiple files from a compound object
        that will be added to a single record.  For example, multiple postcard
        images (front an back). Note that this function must assume the file type
        because the file type is not exported by contentdm for compound object pages.
        Since our compound objects in contentdm are jp2 files, the .jp2 extension
        is appended below.
        :param cdmid_el: Element containing the record's contentdm pointer
        :param current_dir: the current working directory
        :param record: the record to process
        :param collection: the contentdm collection name
        :return:
        """
        # the structure element contains pages
        structure = record.find(FetchBitstreams.cdm_struc['compound_object_container'])
        # get all pages.
        pages = structure.findall('.//' + FetchBitstreams.cdm_struc['compound_object_page'])
        page_count = 0
        thumb_created = False
        for page in pages:
            # get the cdm pointer for the page
            file_el = page.find(FetchBitstreams.cdm_struc['compound_object_page_pointer'])
            # get the files information for the page
            files = page.findall('.//' + FetchBitstreams.cdm_struc['compound_object_page_file'])

            for file in files:
                # get the file type and process the access images and thumbnails
                file_type_el = file.find(FetchBitstreams.cdm_struc['compound_object_page_file_type'])
                # access file
                if file_type_el.text == FetchBitstreams.cdm_struc['compound_object_access_file']:
                    # append .jp2 extension.
                    image_file = file_el.text + '.jp2'
                    print(image_file)
                    FetchBitstreams.add_image_bitstream(file_el,
                                                        image_file,
                                                        current_dir,
                                                        collection,
                                                        page_count)
                    if not thumb_created:
                        FetchBitstreams.create_thumbnail(current_dir, image_file)
                        thumb_created = True
                # thumbnail file
                # if file_type_el.text == FetchBitstreams.cdm_struc['compound_object_thumb_file']:
                #     # set file name to pointer plus extension
                #     ptr = file_el.text
                #     file_name = ptr + '.jpg'
                #     FetchBitstreams.create_thumbnail(current_dir, file_name)

                page_count += 1

    @staticmethod
    def fetch_single_bitstream(cdmid_el, current_dir, record, collection):

        cdmfile_el = record.find(FetchBitstreams.cdm_struc['filename'])

        # thumb_url_el = record.find(FetchBitstreams.cdm_struc['thumbnail'])
        FetchBitstreams.add_image_bitstream(cdmid_el, cdmfile_el.text, current_dir, collection, 0)
        FetchBitstreams.create_thumbnail(current_dir, cdmfile_el.text)
        # FetchBitstreams.add_thumbnail(cdmid_el.text, cdmfile_el.text, thumb_url_el, current_dir, collection, 1)

    @staticmethod
    def fetch_bit_streams(current_dir, record, collection, multiple):
        # type: (str, Element, str, bool) -> None
        """
        Extract the bitstream url from metadata, fetch the bitstream, and add to simple archive format entry.
        If a thumbnail image url is available, repeat operation for the thumbnail. This function throws and error
        if called for a compound object.
        :param current_dir: the full path to the saf output directory
        :param record: the etree element for a contentdm record
        :param collection: the contentdm collection name
        :param multiple: indicates whether to retrieve multiple separate bitstreams from compound object
        """
        cdm_struc = Fields.cdm_structural_elements
        cdmid_el = record.find(cdm_struc['id'])
        if cdmid_el is None:
            print('Error: no cdmid found')
        else:
            if cdmid_el is not None:
                if multiple:
                    # process the compound object data and add multiple bitstreams to the saf directory
                    FetchBitstreams.fetch_multiple_bitsteams(cdmid_el, current_dir, record, collection)
                else:
                    # process as a single item record (compound object bitstreams will be a single thumbnail
                    # image and the full text transcription.
                    FetchBitstreams.fetch_single_bitstream(cdmid_el, current_dir, record, collection)

                # being nice, but this also works running full speed ahead.
                time.sleep(.200)
