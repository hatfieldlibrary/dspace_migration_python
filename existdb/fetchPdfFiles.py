
from urllib.request import urlopen
import urllib.error
from contextlib import contextmanager
from existDbFields import ExistDbFields


def write_pdf_to_contents(out_dir, file_name):

    # self.append_canvas_json(height, width, page_count)
    # Add text file to the saf contents file.
    with open(out_dir + '/contents', 'a') as contents:
        # Add Alto to dspace bundle name OtherContent).
        contents.write(file_name + '\tprimary:true\n')
        contents.close()


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

    # fetch_file assumes that the PDF file is in the eXist-db. This isn't always true. When
    # a file is not found this method will log a 404 error. Generally, this method should not be called
    # for a collection with no  item-level PDF files.
    def fetch_file(self, file_name, collection, out_dir):
        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/pdf/' + file_name

        try:
            with self.closing(urlopen(URL)) as url:
                with open(out_dir + '/' + file_name, 'wb') as f:
                    f.write(url.read())

            out_dir + '/' + file_name
            write_pdf_to_contents(out_dir, file_name)

        except urllib.error as err:
            print('An error occurred fetching file for %s: %s.' % (URL, err))
            self.analyzer.add_pdf_processing_failed(out_dir + ': ' + URL)

        except IOError as err:
            print('An error occurred writing contents to saf for: %s. See %s' % ('thumb.jpg', out_dir))
            print('IO Error: {0}'.format(err))
            self.analyzer.add_pdf_processing_failed(out_dir + ': ' + URL)



