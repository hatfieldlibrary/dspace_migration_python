
class ExistAnalyzer:

    image_encoding_failures = []
    alto_processing_failures = []
    pdf_processing_failures = []

    def __init__(self):
        pass

    def add_alto_processing_failed(self, url):
        self.alto_processing_failures.append(url)

    def add_pdf_processing_failed(self, url):
        self.pdf_processing_failures.append(url)

    def add_image_encoding_failed(self, url):
        self.image_encoding_failures.append(url)

    def print_image_encoding_failures(self):
        if len(self.image_encoding_failures) > 0:
            print('Image Encoding Failures:\n')
            for failure in self.image_encoding_failures:
                print(failure + '\n')

    def print_alto_processing_failures(self):
        if len(self.alto_processing_failures) > 0:
            print('ALTO Processing Failures:\n')
            for failure in self.alto_processing_failures:
                print(failure + '\n')

    def print_pdf_processing_failures(self):
        if len(self.pdf_processing_failures) > 0:
            print('PDF Processing Failures:\n')
            for failure in self.pdf_processing_failures:
                print(failure + '\n')

