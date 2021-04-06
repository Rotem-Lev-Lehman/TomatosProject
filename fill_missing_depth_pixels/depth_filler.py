import cv2
import numpy as np
import os
from pathlib import Path
import gdal
from tqdm import tqdm

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\New_Data\guy"
images_dir_path = fr"{main_path}\Cut_images"


def get_neighbors(depth_img, x, y, radius):
    all_neighbors = np.array([[depth_img[i][j] if 0 <= i < len(depth_img) and 0 <= j < len(depth_img[0]) else 0
                               for j in range(y - radius, y + radius + 1)]
                              for i in range(x - radius, x + radius + 1)])
    all_neighbors = all_neighbors.reshape(-1, )
    non_zero_neighbors = all_neighbors[all_neighbors > 0]
    return non_zero_neighbors


def get_neighbors_vals(depth_img, x, y):
    done = False
    radius = 1
    neighbors = None
    while not done:
        neighbors = get_neighbors(depth_img, x, y, radius)
        if len(neighbors) > 0:
            done = True
        radius += 1
    return neighbors


def get_chosen_value(neighbors_vals):
    # get the min_val of the neighbors:
    return neighbors_vals.min()


def fill_depth(depth_img_path):
    depth_img = gdal.Open(depth_img_path).ReadAsArray()
    depth_0_mask = depth_img == 0
    indices = np.where(depth_0_mask)
    for x, y in zip(indices[0], indices[1]):
        neighbors_vals = get_neighbors_vals(depth_img, x, y)
        chosen_value = get_chosen_value(neighbors_vals)
        depth_img[x, y] = chosen_value
    return depth_img


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if f == 'bgr_image.png']
    return files


rgb_images_names = get_all_files(images_dir_path)

for rgb_img_path in tqdm(rgb_images_names):
    dir_path = os.path.dirname(rgb_img_path)
    depth_img_path = fr'{dir_path}/tiff_depth_image.tiff'
    # img_name = cut_img_name.split('_color_0')[0] + '_color_0'
    # depth_image_path = rgb_img_path.split('_color_0')[0] + '_depth_0.tiff'

    depth_img = fill_depth(depth_img_path)
    rescaled_img = depth_img * (255.0 / depth_img.max())
    img_rgb_depth = np.zeros((depth_img.shape[0], depth_img.shape[1], 3))
    img_rgb_depth[:, :, 0] = rescaled_img
    img_rgb_depth[:, :, 1] = rescaled_img
    img_rgb_depth[:, :, 2] = rescaled_img
    i=0
