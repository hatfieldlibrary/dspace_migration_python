
import urllib.request
import json
from contextlib import contextmanager
from wand.image import Image

from .analyzer import ExistAnalyzer
from .existDbFields import ExistDbFields


class FetchPageImages:

    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    info = {}

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
        print('New Document')
        # initialize info dict
        # self.info = {
        #     "globalDefaults": {
        #         "activated": False,
        #         "label": "",
        #         "width": 0,
        #         "height": 0
        #     },
        #     "canvases": [],
        #     "structures": []
        # }
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
                    print(file_name)
                    if not dry_run:
                        self.fetch_file(file_name, collection, item_id, out_dir, page_count)
                        print(str(page_count))
                        page_count += 1
        # self.write_info_json(out_dir)

    # def write_info_json (self, out_dir):
    #     with open(out_dir + '/info.json', 'w') as contents:
    #         contents.write(json.dumps(self.info))
    #         contents.close()
    #     with open(out_dir + '/contents', 'a') as contents:
    #         contents.write('info.json' + '\tbundle:IIIF\n')
    #         contents.close()

    # def append_canvas_json(self, height, width, page_count):
    #     print('Page ' + str(page_count))
    #     canvas = {'label': 'Page ' + str(page_count), 'width': width, 'height': height, 'pos': page_count}
    #     self.info['canvases'].append(canvas)

    def write_contents(self, out_dir, file_name, page_count):
        print('attempting file read: ' + out_dir + '/' + file_name)
        height = 0
        width = 0
        try:
            with Image(filename='temp.jpg') as f:
                width = f.width
                height = f.height
        except:
            print('An error occurred when reading image size.')
        try:
            # self.append_canvas_json(height, width, page_count)
            # Add text file to the saf contents file.
            with open(out_dir + '/contents', 'a') as contents:
                # Add image to dspace bundle name ORIGINAL).
                contents.write(file_name)
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
        with self.closing(urllib.request.urlopen(URL)) as url:
            with open(out_dir + '/' + file_name, 'wb') as f:
                f.write(url.read())
        try:
            out_dir + '/' + file_name
            self.write_contents(out_dir, file_name, page_count)
        except:
            print('An error occurred writing to content file for %s: %s.' % (out_dir, URL))
            self.analyzer.add_image_encoding_failed(out_dir + ': ' + URL)
