import os
import unittest

from image_processing import mask, tile, utils


class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        self.files_root = "./tests/test_files/"
        self.X = tile.TILE_X
        self.Y = tile.TILE_Y
        pass

    def tearDown(self):
        pass

    def test_masking(self):
        """
        NOTE: test masking file we have been given needs to be shifted to the
        left to be usable
        :return:
        """
        mask_path = mask.get_mask_path(self.X, self.Y, "sugarcane-region")
        my_mask = mask.Mask(mask_path)
        my_mask.rotate(0)
        my_mask.save_image(os.path.join(self.files_root, "mask.png"))

        tile_paths = tile.get_timeseries_image_paths(self.X, self.Y, "TCI")
        my_tile = tile.Tile(tile_paths[0])
        my_tile.save_image(os.path.join(self.files_root, "orig.png"))
        for r in range(5):
            my_mask.rotate(90)
            masked_tile = my_mask.apply_mask(my_tile)
            path = os.path.join(self.files_root, f"{90*r}_masked_tile.png")
            masked_tile.save_image(path)
            self.assertTrue(os.path.isfile(path))

        my_mask.flip_horizontal()
        for r in range(5):
            my_mask.rotate(90)
            masked_tile = my_mask.apply_mask(my_tile)
            path = os.path.join(self.files_root, f"{90*r}_horiz_masked_tile.png")
            masked_tile.save_image(path)
            self.assertTrue(os.path.isfile(path))

        my_mask.flip_vertical()
        for r in range(5):
            my_mask.rotate(90)
            masked_tile = my_mask.apply_mask(my_tile)
            path = os.path.join(self.files_root, f"{90*r}_vert_masked_tile.png")
            masked_tile.save_image(path)
            self.assertTrue(os.path.isfile(path))

    def test_gif_creation(self):
        tile_paths = tile.get_timeseries_image_paths(self.X, self.Y, "TCI")
        gif_file = os.path.join(self.files_root, "unmasked.gif")
        utils.make_gif(image_paths=tile_paths, gif_save_path=gif_file)
        self.assertTrue(os.path.isfile(gif_file))


if __name__ == "__main__":
    unittest.main()
