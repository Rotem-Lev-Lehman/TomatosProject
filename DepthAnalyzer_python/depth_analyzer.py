import cv2
import numpy as np
import os
from pathlib import Path
import gdal
from tqdm import tqdm

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data_depth_no_rec\Week3\Camera1\Rows2_5"

original_images_path = fr"{main_path}\Raw_data\Rows"
cut_images_path = fr"{main_path}\JPEGS"
output_cut_images_dir_path = fr"{main_path}\Cut_images"
Path(output_cut_images_dir_path).mkdir(parents=True, exist_ok=True)


def find_and_save_cuts(original_image_path, cut_image_path, depth_image_path, prev_image_name, confidence):
    regular_img = cv2.imread(original_image_path)
    cut_img = cv2.imread(cut_image_path)
    depth_img = gdal.Open(depth_image_path).ReadAsArray()

    result = cv2.matchTemplate(regular_img, cut_img, cv2.TM_CCOEFF_NORMED)
    rev = False

    if result.max() < confidence:
        # need to flip image:
        cut_img = cv2.rotate(cut_img, cv2.ROTATE_180)
        result = cv2.matchTemplate(regular_img, cut_img, cv2.TM_CCOEFF_NORMED)
        if result.max() < confidence:
            raise Exception('Tried to flip but still could not find a match!')
        rev = True

    top_left_coor = np.unravel_index(result.argmax(), result.shape)
    bottom_right_coor = np.array(cut_img.shape[:2]) + np.array(top_left_coor)

    # subset = regular_img[top_left_coor[0]:bottom_right_coor[0], top_left_coor[1]:bottom_right_coor[1], :]

    # cv2.imshow('regular image', regular_img)
    # cv2.imshow('cut image', cut_img)
    # cv2.imshow('subset image', subset)
    # cv2.waitKey(0)

    cut_section_BGR = regular_img[top_left_coor[0]:bottom_right_coor[0], top_left_coor[1]:bottom_right_coor[1], :]
    cut_section_Depth = depth_img[top_left_coor[0]:bottom_right_coor[0], top_left_coor[1]:bottom_right_coor[1]]

    img_files_base_path = fr"{output_cut_images_dir_path}\{prev_image_name}"
    Path(img_files_base_path).mkdir(parents=True, exist_ok=True)

    bgr_img_out_path = fr"{img_files_base_path}\bgr_image.png"
    depth_img_out_path = fr"{img_files_base_path}\depth_image.png"
    depth_tiff_out_path = fr"{img_files_base_path}\tiff_depth_image.tiff"

    cv2.imwrite(bgr_img_out_path, cut_section_BGR)
    cv2.imwrite(depth_img_out_path, cut_section_Depth)
    cv2.imwrite(depth_tiff_out_path, cut_section_Depth)


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] in ['.png', '.jpeg']]
    return files


cut_images_names = get_all_files(cut_images_path)
original_images_names = get_all_files(original_images_path)

img_name2path = {}

for img_path in original_images_names:
    filename = os.path.basename(img_path)
    img_name = filename.split('.')[0]
    img_name2path[img_name] = img_path

for cut_image_path in tqdm(cut_images_names):
    filename = os.path.basename(cut_image_path)
    cut_img_name = filename.split('.')[0]
    img_name = cut_img_name.split('color_0')[0] + 'color_0'
    original_image_path = img_name2path[img_name]
    depth_image_path = original_image_path.split('color_0')[0] + 'depth_0.tiff'

    find_and_save_cuts(original_image_path, cut_image_path, depth_image_path, cut_img_name, confidence=0.95)
