
import urllib.request
from contextlib import contextmanager
from wand.image import Image

from .analyzer import ExistAnalyzer
from .existDbFields import ExistDbFields


def write_image_contents(out_dir, file_name, label, page_count):
    # print('attempting file read: ' + out_dir + '/' + file_name)
    height = 0
    width = 0
    # try:
    #     with Image(filename='temp.jpg') as f:
    #         width = f.width
    #         height = f.height
    # except:
    #     print('An error occurred when reading image size.')
    try:
        # self.append_canvas_json(height, width, page_count)
        # Add text file to the saf contents file.
        with open(out_dir + '/contents', 'a') as contents:
            # Add image to dspace bundle name ORIGINAL).
            if len(label) > 0:
                contents.write(file_name + '\tbundle:iiif\tiiif-label:' + label + '\n')
            else:
                contents.write(file_name + '\tbundle:iiif\n')
            contents.close()
    except IOError as err:
        print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
        print('IO Error: {0}'.format(err))
    except Exception as err:
        print('An error occurred writing contents for: %s. See %s' % ('thumb.jpg', out_dir))
        print('Exception: {0}'.format(err))


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
        # type: (Element, str, str, str, bool) -> None

        if element is None:
            print('Missing XML node for %s' % item_id)
            print('Cannot retrieve jp2 images for the item.')
            return

        struct_search = './' + self.mets_fields.mets_structural_elements['struct_map'] + '/' + self.mets_fields.mets_structural_elements['mets_div'] + '//' + self.mets_fields.mets_structural_elements['mets_div']
        page_types = element.findall(struct_search, self.ns)
        type_arr = []
        for typeElem in page_types:
            if 'LABEL' in typeElem.attrib:
                label = typeElem.attrib['LABEL']
                if len(label) > 0:
                    type_arr.append(label)

        page_sec = element.find(self.mets_fields.mets_structural_elements['file_section'], self.ns)
        # the file groups
        pages = page_sec.findall('.//' + self.mets_fields.mets_structural_elements['file_group'], self.ns)
        page_count = 1
        for page in pages:
            files = page.iterfind(self.mets_fields.mets_structural_elements['file'], self.ns)
            foldout_count = 1
            for file in files:
                # the service file
                if file.attrib['USE'] == 'service' or file.attrib['USE'] == 'foldout':
                    location = file.find(self.mets_fields.mets_structural_elements['file_location'], self.ns)
                    # the file name
                    file_name = location.attrib[self.mets_fields.mets_structural_elements['file_href']]
                    # print(file_name)
                    if not dry_run:
                        label = ''
                        if len(type_arr) >= page_count:
                            label = type_arr[page_count - 1]
                        if file.attrib['USE'] == 'foldout':
                            label = '- Foldout ' + str(foldout_count)
                            foldout_count += 1
                        self.fetch_file(file_name, label, collection, item_id, out_dir, page_count)
                        # print(str(page_count))
                        if file.attrib['USE'] == 'service':
                            page_count += 1

    def fetch_file(self, file_name, label, collection, item_id, out_dir, page_count):
        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/images/' + item_id + '/' + file_name
        #  print(URL)

        image_found = False

        try:
            with self.closing(urllib.request.urlopen(URL)) as url:
                with open(out_dir + '/' + file_name, 'wb') as f:
                    f.write(url.read())
                    image_found = True

        except Exception as err:
            print('An error occurred fetching image file for %s: %s.' % (URL, err))
            self.analyzer.add_pdf_processing_failed(out_dir + ': ' + URL)

        try:
            if image_found:
                out_dir + '/' + file_name
                write_image_contents(out_dir, file_name, label, page_count)
        except IOError as err:
            print('An error occurred writing to content file for %s: %s.' % (URL, err))
            self.analyzer.add_image_encoding_failed(out_dir + ': ' + URL)
