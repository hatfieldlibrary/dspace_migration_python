from _elementtree import Element
from wand.image import Image
import urllib.request
from contextlib import contextmanager

from .analyzer import ExistAnalyzer
from .existDbFields import ExistDbFields


class FetchThumbnailImage:

    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    @contextmanager
    def closing(self, thing):
        try:
            yield thing
        finally:
            thing.close()

    def __init__(self, analyzer, create_thumbnail):
        assert isinstance(analyzer, ExistAnalyzer), "%r is not a print queue" % analyzer
        self.analyzer = analyzer
        self.create_thumbnail = create_thumbnail
        self.mets_fields = ExistDbFields()

    def convert_file(self, file_name, collection, item_id, out_dir):

        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/images/' + item_id + '/' + file_name
        response = urllib.request.urlopen(URL)
        # write the file to a temporary on disk location.
        with self.closing(urllib.request.urlopen(URL)):
            with Image(file=response) as f:
                f.format = 'jpeg'
                f.save(filename='temp.jpg')
        try:
            with Image(filename='temp.jpg') as f:
                f.resize(200)
                f.save(filename=out_dir + '/thumb.jpg.jpg')
                self.write_contents(out_dir)
        except Exception as err:
            print('An error occurred converting image for %s: %s.' % (out_dir, URL))
            print(err)
            self.analyzer.add_image_encoding_failed(out_dir + ': ' + URL)

    @staticmethod
    def write_contents(out_dir):
        try:
            # Add text file to the saf contents file.
            with open(out_dir + '/contents', 'a') as contents:
                contents.write('thumb.jpg.jpg' + '\tbundle:THUMBNAIL\n')
                contents.close()
        except IOError as err:
            print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg.jpg', out_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            print('An error occurred writing contents for: %s. See %s' % ('thumb.jpg.jpg', out_dir))
            print('Exception: {0}'.format(err))

    def fetch_thumbnail(self, element, collection, item_id, out_dir, dry_run):
        # type: (Element) -> None
        if element is None:
            print('missing root')
        # the file section
        page_sec = element.find(self.mets_fields.mets_structural_elements['file_section'], self.ns)
        # the file groups
        pages = page_sec.findall('.//' + self.mets_fields.mets_structural_elements['file_group'], self.ns)
        # the files from the first file group (page one)
        files = pages[0].iterfind(self.mets_fields.mets_structural_elements['file'], self.ns)
        file_name = ''
        for file in files:
            # the service file for the first page
            if file.attrib['USE'] == 'service':
                location = file.find(self.mets_fields.mets_structural_elements['file_location'], self.ns)
                # the file name of the first page.
                file_name = location.attrib[self.mets_fields.mets_structural_elements['file_href']]
                break

        if len(file_name) > 0:
            if not dry_run and self.create_thumbnail:
                self.convert_file(file_name, collection, item_id, out_dir)
