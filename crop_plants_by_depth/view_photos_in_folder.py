import cv2
import os
from tqdm import tqdm
import pandas as pd


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] in ['.png', '.jpeg']]
    return files


def view_images(original_img_path, cropped_img_path):
    original_img = cv2.imread(original_img_path)
    cropped_img = cv2.imread(cropped_img_path)
    cv2.imshow("original", original_img)
    cv2.imshow("cropped", cropped_img)
    cv2.waitKey(0)


# main_folder_path = r'C:\Users\User\Desktop\second_degree\tomatos_project\Progress\New_Data\guy'
# original_images_path = fr'{main_folder_path}\images'
# cropped_images_path = fr'{main_folder_path}\Cut_images'
# original_images_names = get_all_files(original_images_path)
#
# for img_path in tqdm(original_images_names):
#     filename = os.path.basename(img_path)
#     cropped_img_folder_name = filename.split('.')[0]
#     cropped_img_path = fr'{cropped_images_path}\{cropped_img_folder_name}\bgr_image.png'
#     print(f'Current img name: {cropped_img_folder_name}')
#     view_images(img_path, cropped_img_path)

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress"

original_images_path = fr"{main_path}\Data\All_cut_images"

cropped_images_path = fr"{main_path}\April_stuff\week3_cropped_with_depth"
csv_images_names = fr"{main_path}\April_stuff\week3_guy_shani.txt"

df_filenames = pd.read_csv(csv_images_names, header=None)
filenames = df_filenames[1]
images_names = list(filenames.apply(lambda x: x.split('_zssr')[0]))

for img_name in tqdm(images_names):
    original_rgb_img_path = fr'{original_images_path}\{img_name}\bgr_image.png'
    cropped_rgb_img_path = fr'{cropped_images_path}\{img_name}\bgr_image.png'
    print(f'Current img name: {img_name}')
    view_images(original_rgb_img_path, cropped_rgb_img_path)
