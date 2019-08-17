from PIL import Image

from .tile import Tile

# The expected value of a Pixel in a mask file indicating that the pixel is
# within that region.  Tuple value, (Red, Green, Blue, Alpha)
IS_IN_MASK_PIXEL_VALUE = (0, 0, 0, 255)

MASK_X = 48
MASK_Y = 3


class Mask(Tile):
    def apply_mask(self, image: Tile) -> Tile:
        masked_tile = Tile()
        masked_tile.image = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        # note: here self.image is the mask's image
        masked_tile.image = Image.composite(
            image1=image.image, image2=masked_tile.image, mask=self.image
        )
        return masked_tile

    def is_in_mask(self, pixel_x, pixel_y):
        if self.pixels[pixel_y, pixel_x] == IS_IN_MASK_PIXEL_VALUE:
            return True
        else:
            return False

    def print_ascii_mask(self):
        """
        Print out an ascii representation of the map
        """
        # We don't really want to display ASCII art that is 512 characters long as it will be
        # too long to show in a terminal, so lets scale it
        scale_factor = 10

        width_in_chars = int(self.width / scale_factor)
        height_in_chars = int(self.height / scale_factor)

        for x_char in range(0, width_in_chars - 1):
            for y_char in range(0, height_in_chars - 1):
                # Convert the character index back to actual pixels
                pixel_x = x_char * scale_factor
                pixel_y = y_char * scale_factor

                # is the pixel in my mask?
                in_mask = self.is_in_mask(pixel_x, pixel_y)
                if in_mask:
                    print("X", end="")
                else:
                    print(" ", end="")

            # Print a newline at the end of each row
            print("\n", end="")


# Get the physical path to the PNG image containing the mask file
def get_mask_path(tile_x, tile_y, mask_type):
    path = f"./data/sentinel-2a-tile-{tile_x}x-{tile_y}y/masks/{mask_type}-mask.png"
    return path
