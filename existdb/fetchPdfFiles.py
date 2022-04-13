import urllib
from contextlib import contextmanager

from existDbFields import ExistDbFields

def write_pdf_to_contents(out_dir, file_name):

    try:
        # self.append_canvas_json(height, width, page_count)
        # Add text file to the saf contents file.
        with open(out_dir + '/contents', 'a') as contents:
            # Add Alto to dspace bundle name OtherContent).
            contents.write(file_name + '\n')
            contents.close()

    except IOError as err:
        print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
        print('IO Error: {0}'.format(err))


class FetchPdfFiles:

    @contextmanager
    def closing(self, thing):
        try:
            yield thing
        finally:
            thing.close()

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.mets_fields = ExistDbFields()

    def fetch_files(self, file_name, collection, out_dir, dry_run):
        if not dry_run:
            self.fetch_file(file_name, collection, out_dir)

    def fetch_file(self, file_name, collection, out_dir):
        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/pdf/' + file_name

        with self.closing(urllib.request.urlopen(URL)) as url:
            with open(out_dir + '/' + file_name, 'wb') as f:
                f.write(url.read())

        try:
            out_dir + '/' + file_name
            write_pdf_to_contents(out_dir, file_name)
        except:
            print('An error occurred writing to content file for %s: %s.' % (out_dir, URL))
            self.analyzer.add_alto_processing_failed(out_dir + ': ' + URL)
