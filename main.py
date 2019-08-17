import logging
import os

from image_processing import mask, tile, utils
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def mask_files():
    """
    Loads in Tiles for phase 1
    makes a gif of the tiles
    masks tiles them with the sugarcane mask
    saves the masked tiles
    makes a gif of the masked_tiles
    """

    # setting root files
    gif_save_dir = "./demo_files/"
    masked_files_save_dir = "data/sentinel-2a-tile-7680x-10240y/masked_timeseries/"

    tile_paths = tile.get_timeseries_image_paths(tile.TILE_X, tile.TILE_Y, "TCI")
    num_files = len(tile_paths)
    logging.info(f"Loading {num_files} tiles")
    utils.make_gif(tile_paths, os.path.join(gif_save_dir, "timeseries.gif"))

    mask_type = "sugarcane-region"
    logging.info(f"Loading mask {mask_type}")
    mask_path = mask.get_mask_path(tile.TILE_X, tile.TILE_Y, mask_type)
    my_mask = mask.Mask(mask_path)
    my_mask.translate(
        mask.MASK_X, mask.MASK_Y
    )  # for proper placement of mask on top of data

    logging.info(f"Applying mask to tiles")
    tiles = [tile.Tile(p) for p in tile_paths]
    tile_filenames = [os.path.basename(p) for p in tile_paths]
    masked_filenames = [
        os.path.join(masked_files_save_dir, "masked_" + p) for p in tile_filenames
    ]
    masked_tiles = [my_mask.apply_mask(t) for t in tiles]
    for i in tqdm(range(num_files)):
        masked_tiles[i].save_image(masked_filenames[i])
    utils.make_gif(
        masked_filenames, os.path.join(gif_save_dir, "masked_timeseries.gif")
    )


def main():
    mask_files()


if __name__ == "__main__":
    main()
