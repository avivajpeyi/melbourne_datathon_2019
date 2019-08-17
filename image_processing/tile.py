import logging
from typing import List, Optional
import os
import glob
from PIL import Image

# The initial release contains only one tile, so lets hardcode its location
# here.  When you have more tiles, you can update this
TILE_X = 7680
TILE_Y = 10240

# Tile width / height in pixels
WIDTH_PX = 512
HEIGHT_PX = 512

class Tile():
    def __init__(self, filename:Optional[str]=None):
        self.width = WIDTH_PX
        self.height = HEIGHT_PX
        if filename:
            self.filename = filename

    @property
    def filename(self):
        return self._filename

    def rotate(self, angle):
        self.image =  self.image.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)

    @filename.setter
    def filename(self, filename):
        if os.path.isfile(filename):
            self._filename = filename
            self.image = Image.open(self.filename)
        else:
            raise FileNotFoundError("Sorry invalid file")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image: Image):
        self._image = image
        pass

    @property
    def pixels(self):
        return self.image.load()

    def save_image(self, filepath):
        dir = os.path.dirname(filepath)
        if not os.path.isdir(dir):
            os.mkdir(dir)
        self.image.save(filepath)
        self.filename = filepath


# Get a list of all the image tiles for a specific x,y coordinate
# for the specified band
def get_timeseries_image_paths(tile_x, tile_y, band):
    path = f"./data/sentinel-2a-tile-{tile_x}x-{tile_y}y/timeseries/{tile_x}-{tile_y}-{band}*.png"
    logging.info(f"Searching for images in {path}")
    images = glob.glob(path)
    return images



