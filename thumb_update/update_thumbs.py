import os
import xml.etree.ElementTree as ET
from wand.image import Image


def create_thumbnail(current_dir, input_jp2):
    try:
        with Image(filename=current_dir + '/' + input_jp2) as f:
            f.format = 'jpeg'
            f.save(filename='temp.jpg')
    except Exception as err:
        print('An error occurred when creating temp file: %s' % err)
    try:
        with Image(filename='temp.jpg') as f:
            height = f.height
            width = f.width
            ratio = float(f.width) / float(f.height)
            if height > width:
                if height > 175:
                    height = 175
                    width = int(175.0 * ratio)
            else:
                if width > 175:
                    width = 175
                    height = int(175.0 / ratio)

            f.resize(width, height)
            f.save(filename=current_dir + '/thumb.jpg.jpg')

    except Exception as err:
        print('An error occurred converting image for: %s.' % current_dir)
        print(err)


class UpdateThumbs:

    def __init__(self, saf_directory, repo, batch):
        self.saf_directory = saf_directory
        self.repo = repo
        self.batch = batch

    def update_thumbs(self):
        base_directory = os.path.abspath(os.getcwd())
        in_dir = base_directory + '/' + self.repo + '/saf/manuscripts/' + self.saf_directory + '/' + self.batch

        for saf_dir in os.listdir(in_dir):
            current_dir = in_dir + '/' + saf_dir
            for file in os.listdir(current_dir):
                if file.endswith(".jp2"):
                    create_thumbnail(current_dir, file)
                    break




