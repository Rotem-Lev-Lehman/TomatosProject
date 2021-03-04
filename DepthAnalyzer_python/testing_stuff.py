import cv2
import numpy as np
import os
from pathlib import Path
import gdal

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data_depth_no_rec\Week4\Camera2\All_rows"
cut_images_dir_path = fr"{main_path}\Cut_images"
img_name = "20200924_171548_color_0_375_77_614_420"

base_img_dir_path = fr"{cut_images_dir_path}\{img_name}"
bgr_image_path = fr"{base_img_dir_path}\bgr_image.png"
depth_png_image_path = fr"{base_img_dir_path}\depth_image.png"
depth_tiff_image_path = fr"{base_img_dir_path}\tiff_depth_image.tiff"

bgr_img = cv2.imread(bgr_image_path)
depth_png_img = cv2.imread(depth_png_image_path)
depth_tiff_img = gdal.Open(depth_tiff_image_path).ReadAsArray()

cv2.imshow("bgr image", bgr_img)
bgr_img[depth_tiff_img == 0] = (255, 0, 0)
cv2.imshow("bgr-depth image", bgr_img)
cv2.waitKey(0)
