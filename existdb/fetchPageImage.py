
import urllib
from contextlib import contextmanager
from pgmagick import Image

from .analyzer import ExistAnalyzer
from .existDbFields import ExistDbFields


class FetchPageImages:

    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    @contextmanager
    def closing(self, thing):
        try:
            yield thing
        finally:
            thing.close()

    def __init__(self, analyzer):
        assert isinstance(analyzer, ExistAnalyzer), "%r is not a print queue" % analyzer
        self.analyzer = analyzer
        self.mets_fields = ExistDbFields()

    def fetch_images(self, element, collection, item_id, out_dir, dry_run):
        # type: (Element) -> None
        if element is None:
            print('missing root')
        # the file section
        page_sec = element.find(self.mets_fields.mets_structural_elements['file_section'], self.ns)
        # the file groups
        pages = page_sec.findall('.//' + self.mets_fields.mets_structural_elements['file_group'], self.ns)
        page_count = 1
        for page in pages:
            files = page.iterfind(self.mets_fields.mets_structural_elements['file'], self.ns)
            for file in files:
                # the service file
                if file.attrib['USE'] == 'service':
                    location = file.find(self.mets_fields.mets_structural_elements['file_location'], self.ns)
                    # the file name
                    file_name = location.attrib[self.mets_fields.mets_structural_elements['file_href']]
                    if not dry_run:
                        self.fetch_file(file_name, collection, item_id, out_dir, page_count)
                        page_count += 1

    @staticmethod
    def write_contents(out_dir, file_name, page_count):
        print('attempting file read: ' + out_dir + '/' + file_name)
        height = 0
        width = 0
        try:
            with open('temp.jpg', 'r') as f:
                im = Image('temp.jpg')
                width = im.columns()
                height = im.rows()
        except:
            print('An error occurred when reading image size.')
        try:
            # Add text file to the saf contents file.
            with open(out_dir + '/contents', 'a') as contents:
                # Add images to dspace bundle name 'IIIF' and include the page name (based on count).
                contents.write(file_name + '\tbundle:IIIF\tvidescription:Page '
                               + str(page_count) + '-' + str(width) + '-' + str(height) + '\n')
                contents.close()
        except IOError as err:
            print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            print('An error occurred writing contents for: %s. See %s' % ('thumb.jpg', out_dir))
            print('Exception: {0}'.format(err))

    def fetch_file(self, file_name, collection, item_id, out_dir, page_count):
        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/images/' + item_id + '/' + file_name
        print(URL)
        # write the file to a temporary on disk location.
        with self.closing(urllib.urlopen(URL)) as url:
            with open(out_dir + '/' + file_name, 'wb') as f:
                f.write(url.read())
        try:
            out_dir + '/' + file_name
            self.write_contents(out_dir, file_name, page_count)
        except:
            print('An error occurred writing to content file for %s: %s.' % (out_dir, URL))
            self.analyzer.add_image_encoding_failed(out_dir + ': ' + URL)
