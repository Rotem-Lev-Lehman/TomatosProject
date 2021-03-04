import cv2
import numpy as np
import os

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data_depth_no_rec\Week4\Camera2\All_rows"

original_images_path = fr"{main_path}\Raw_data\Rows"
cut_images_path = fr"{main_path}\JPEGS"
rectangles_output_path = fr"{main_path}\New_rectangles\Rectangles.txt"


def find_rectangle(original_image_path, cut_image_path, confidence):
    regular_img = cv2.imread(original_image_path)
    cut_img = cv2.imread(cut_image_path)

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
    rectangle_coordination_str = f'[{top_left_coor[1]},{top_left_coor[0]},{bottom_right_coor[1]},{bottom_right_coor[0]}'
    if rev:
        rectangle_coordination_str += ' - reversed'
    rectangle_coordination_str += ']'

    return rectangle_coordination_str


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] in ['.png', '.jpeg']]
    return files


def save_rectangles_file(original_img_paths, img_path2coordinations, rectangles_output_path):
    with open(rectangles_output_path, 'w') as out_file:
        for img_path in original_img_paths:
            coordinations_arr = img_path2coordinations[img_path]
            out_file.write(f'{img_path}\t{len(coordinations_arr)}')
            for coor in coordinations_arr:
                out_file.write(f'\t{coor}')
            out_file.write('\n')


cut_images_names = get_all_files(cut_images_path)
original_images_names = get_all_files(original_images_path)

img_name2path = {}
img_path2coordinations = {}

for img_path in original_images_names:
    filename = os.path.basename(img_path)
    img_name = filename.split('.')[0]
    img_name2path[img_name] = img_path
    img_path2coordinations[img_path] = []

for cut_image_path in cut_images_names:
    filename = os.path.basename(cut_image_path)
    cut_img_name = filename.split('.')[0]
    img_name = cut_img_name.split('color_0')[0] + 'color_0'
    original_image_path = img_name2path[img_name]

    curr_coordination = find_rectangle(original_image_path, cut_image_path, confidence=0.95)
    img_path2coordinations[original_image_path].append(curr_coordination)

# all of the coordinations for every image are now already found in img_path2coordinations. Lets save it to a file:
save_rectangles_file(original_images_names, img_path2coordinations, rectangles_output_path)

