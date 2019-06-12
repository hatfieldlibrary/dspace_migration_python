from _elementtree import Element
from pgmagick import Image
import urllib
import io
from contextlib import contextmanager

from existDbFields import ExistDbFields

class FetchThumbnailImage:

    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    @contextmanager
    def closing(self, thing):
        try:
            yield thing
        finally:
            thing.close()

    def __init__(self):
        self.mets_fields = ExistDbFields()

    def convert_file(self, file_name, collection, item_id, out_dir):

        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/images/' + item_id + '/' + file_name
        print URL
        with self.closing(urllib.urlopen(URL)) as url:
            with open('temp.jpg', 'wb') as f:
                f.write(url.read())
        im = Image('temp.jpg')
        im.quality(50)
        im.scale('200x200')
        im.write(out_dir + '/thumb.jpg')
        self.write_contents(out_dir)

    def write_contents(self, out_dir):
        try:
            print 'write'
            # Add text file to the saf contents file.
            with open(out_dir + '/contents', 'a') as contents:
                contents.write('thumb.jpg')
                contents.close()
        except IOError as err:
            print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
            print('IO Error: {0}'.format(err))
        except Exception as err:
            print('An error occurred writing contents for: %s. See %s' % ('thumb.jpg', out_dir))
            print 'Exception: {0}'.format(err)

    def fetch_thumbnail(self, element, collection, item_id, out_dir, dry_run):
        # type: (Element) -> None
        if element is None:
            print 'missing root'
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
            if not dry_run:
                self.convert_file(file_name, collection, item_id, out_dir)
