import cv2
import numpy as np
import os
from pathlib import Path
import gdal
import operator

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data"
cut_images_dir_path = fr"{main_path}\All_cut_images"
img_name = "20200924_171321_color_0_26_137_530_434"

base_img_dir_path = fr"{cut_images_dir_path}\{img_name}"
bgr_image_path = fr"{base_img_dir_path}\bgr_image.png"
# depth_png_image_path = fr"{base_img_dir_path}\depth_image.png"
depth_tiff_image_path = fr"{base_img_dir_path}\tiff_depth_image.tiff"

bgr_img = cv2.imread(bgr_image_path)
# depth_png_img = cv2.imread(depth_png_image_path)
depth_tiff_img = gdal.Open(depth_tiff_image_path).ReadAsArray()

percentile = 10
percentile_val = np.percentile(depth_tiff_img[depth_tiff_img != 0], percentile)
range_indices = np.logical_not(np.logical_or(depth_tiff_img > percentile_val, depth_tiff_img == 0))
in_range_indices = np.where(range_indices == True)
min_x = int(np.min(in_range_indices[0]) * 0.9)
max_x = int(np.max(in_range_indices[0]) * 1.1)
min_y = int(np.min(in_range_indices[1]) * 0.9)
max_y = int(np.max(in_range_indices[1]) * 1.1)
cropped_bgr_img = bgr_img[min_x:max_x, min_y: max_y]  # use this image

print(bgr_img.shape)
increased_shape = tuple(map(operator.add, bgr_img.shape, (0, 0, 1)))

rgbd_img = np.zeros(increased_shape)
rgbd_img[:, :, :-1] = bgr_img
rgbd_img[:, :, -1] = depth_tiff_img
cv2.imshow("rgbd image", rgbd_img)

gary2rgb = cv2.cvtColor(depth_tiff_img, cv2.COLOR_GRAY2RGB)
cv2.imshow("only depth image", gary2rgb)
# cv2.imshow("bgr image", bgr_img)
# bgr_img[depth_tiff_img == 0] = (255, 0, 0)
# cv2.imshow("bgr-depth image", bgr_img)
# cv2.waitKey(0)

cv2.imshow("bgr image", bgr_img)
cv2.imshow("cropped bgr image", cropped_bgr_img)
bgr_img[np.logical_or(depth_tiff_img > percentile_val, depth_tiff_img == 0)] = (255, 0, 0)
cv2.imshow("bgr-depth image", bgr_img)
cropped_bgr_img = bgr_img[min_x:max_x, min_y: max_y]
cv2.imshow("cropped bgr-depth image", cropped_bgr_img)
cv2.waitKey(0)
# print()
