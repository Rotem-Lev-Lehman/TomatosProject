import cv2
import random


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


base_folder_path = r'C:\Users\User\Desktop\second_degree\tomatos_project\Progress\April_stuff'
original_plants_directory = fr'{base_folder_path}\super_resolution_all_images'
image_path = fr'{original_plants_directory}\20200903_181642_color_0_2_117_303_468_zssr_X4.00X4.00.jpg'

img = cv2.imread(image_path)
img_show = cv2.resize(img, (500, 500))
cv2.imshow('original_image', img_show)
height, width = img.shape[:-1]
cropped_rectangle_size = 300
same_box_size = 100

height_jumps = height // (cropped_rectangle_size - same_box_size)
width_jumps = width // (cropped_rectangle_size - same_box_size)
for i in range(height_jumps):
    y_start = i * (cropped_rectangle_size - same_box_size)
    y_end = y_start + cropped_rectangle_size
    for j in range(width_jumps):
        x_start = j * (cropped_rectangle_size - same_box_size)
        x_end = x_start + cropped_rectangle_size
        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), random_color(), 5)

img_show = cv2.resize(img, (500, 500))
cv2.imshow('cropped_rectangles', img_show)
cv2.waitKey(0)
