import os
import shutil
import unittest

from image_processing import mask, tile, utils


class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        self.files_root = "./tests/test_files/"
        os.makedirs(self.files_root, exist_ok=True)
        self.X = tile.TILE_X
        self.Y = tile.TILE_Y
        pass

    def tearDown(self):
        shutil.rmtree(self.files_root)

    def test_masking(self):
        """
        NOTE: test masking file we have been given needs to be shifted to the
        left to be usable
        :return:
        """
        mask_path = mask.get_mask_path(self.X, self.Y, "sugarcane-region")
        my_mask = mask.Mask(mask_path)
        my_mask.save_image(os.path.join(self.files_root, "mask.png"))

        tile_paths = tile.get_timeseries_image_paths(self.X, self.Y, "TCI")
        my_tile = tile.Tile(tile_paths[0])
        my_tile.save_image(os.path.join(self.files_root, "orig.png"))

        my_mask.translate(mask.MASK_X, mask.MASK_Y)
        masked_tile = my_mask.apply_mask(my_tile)
        path = os.path.join(self.files_root, f"masked_tile.png")
        masked_tile.save_image(path)
        self.assertTrue(os.path.isfile(path))

    def test_rotation_and_flip(self):
        mask_path = mask.get_mask_path(self.X, self.Y, "sugarcane-region")
        my_mask = mask.Mask(mask_path)
        my_mask.rotate(0)
        my_mask.flip_horizontal()
        my_mask.flip_vertical()
        my_mask.translate(0, 0)

    def test_gif_creation(self):
        tile_paths = tile.get_timeseries_image_paths(self.X, self.Y, "TCI")
        gif_file = os.path.join(self.files_root, "unmasked.gif")
        utils.make_gif(image_paths=tile_paths, gif_save_path=gif_file)
        self.assertTrue(os.path.isfile(gif_file))


if __name__ == "__main__":
    unittest.main()
