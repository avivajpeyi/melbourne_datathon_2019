import os
from PIL import Image


def make_gif(image_paths, gif_save_path):
    """
    save into a GIF file that loops forever
    :param image_paths: list of paths of the images
    :param gif_save_path: the save path of the gif
    :return: None
    """
    gif_dir = os.path.dirname(gif_save_path)
    if not os.path.isdir(gif_dir):
        os.mkdir(gif_dir)
    frames = [Image.open(p) for p in image_paths]
    frames[0].save(gif_save_path, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)