
class ExistAnalyzer:

    image_encoding_failures = []

    def __init__(self):
        pass

    def add_image_encoding_failed(self, url):
        self.image_encoding_failures.append(url)

    def print_image_encoding_failures(self):
        for failure in self.image_encoding_failures:
            print failure
