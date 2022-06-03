import urllib
from contextlib import contextmanager
from existDbFields import ExistDbFields


def write_alto_to_contents(out_dir, file_name):

    try:
        # self.append_canvas_json(height, width, page_count)
        # Add text file to the saf contents file.
        with open(out_dir + '/contents', 'a') as contents:
            # Add Alto to dspace bundle name OtherContent).
            contents.write(file_name + '\tbundle:OtherContent\n')
            contents.close()

    except IOError as err:
        print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
        print('IO Error: {0}'.format(err))


class FetchAltoFiles:

    ns = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3'}

    @contextmanager
    def closing(self, thing):
        try:
            yield thing
        finally:
            thing.close()

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.mets_fields = ExistDbFields()

    def fetch_files(self, element, collection, obj_id,  out_dir, dry_run):

        if element is None:
            print('missing root')

        # the file section
        page_sec = element.find(self.mets_fields.mets_structural_elements['file_section'], self.ns)

        # the file groups
        pages = page_sec.findall('.//' + self.mets_fields.mets_structural_elements['file_group'], self.ns)
        for page in pages:
            files = page.iterfind(self.mets_fields.mets_structural_elements['file'], self.ns)
            for file in files:
                # the service file
                if file.attrib['USE'] == 'ocr':
                    location = file.find(self.mets_fields.mets_structural_elements['file_location'], self.ns)
                    # the file name
                    file_name = location.attrib[self.mets_fields.mets_structural_elements['file_href']]
                    # INSANITY begins. Scrapbook ocr file names are modified in mets. So they don't match
                    # the alto file names. Sara must have added a hack in the xquery API for this collection.
                    # For collection in a series, e.g. Collegian, omit this file name update!
                    # This name update solves the processing problem, BUT, the OCR files in mets and the actual
                    # file names do not match. Either fix this in mets, or (more likely) do not rename the
                    # mets file to 'met.xml'. When indexed for searching the order of ALTO files in
                    # the DSpace bundle will then be used and the mets file ignored.
                    file_name = obj_id + '01' + file_name
                    #file_name = obj_id + file_name
                    # print(file_name)
                    if not dry_run:
                        self.fetch_file(file_name, collection, out_dir)

    def fetch_file(self, file_name, collection, out_dir):

        # this determines partion of the alto file name that is retained. The
        # retained string should match the mets orc file value (e.g. 0001.xml)
        cut_size = 8

        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/alto/' + file_name
       #  print(URL)
        alto_found = False
        # write the file to a temporary on disk location.
        with self.closing(urllib.request.urlopen(URL)) as url:
            file_name = file_name[-cut_size:]
            with open(out_dir + '/' + file_name, 'wb') as f:
                f.write(url.read())
                alto_found = True

        try:
            if alto_found:
                out_dir + '/' + file_name
                write_alto_to_contents(out_dir, file_name)
        except:
            print('An error occurred writing to content file for %s: %s.' % (out_dir, URL))
            self.analyzer.add_alto_processing_failed(out_dir + ': ' + URL)
