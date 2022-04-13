import urllib


def write_alto_to_contents(out_dir, file_name):

    print('attempting file read: ' + out_dir + '/' + file_name)
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

    def fetch_files(self, element, collection, item_id, out_dir, dry_run):

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
                if file.attrib['USE'] == 'service':
                    location = file.find(self.mets_fields.mets_structural_elements['file_location'], self.ns)
                    # the file name
                    file_name = location.attrib[self.mets_fields.mets_structural_elements['file_href']]
                    print(file_name)
                    if not dry_run:
                        self.fetch_file(file_name, collection, item_id, out_dir)

    def fetch_file(self, file_name, collection, item_id, out_dir):

        URL = 'http://exist.willamette.edu:8080/exist/rest/db/' + collection + '/alto/' + file_name
        print(URL)
        # write the file to a temporary on disk location.
        with self.closing(urllib.request.urlopen(URL)) as url:
            with open(out_dir + '/' + file_name, 'wb') as f:
                f.write(url.read())

        try:
            out_dir + '/' + file_name
            write_alto_to_contents(out_dir, file_name)
        except:
            print('An error occurred writing to content file for %s: %s.' % (out_dir, URL))
            self.analyzer.add_image_encoding_failed(out_dir + ': ' + URL)
