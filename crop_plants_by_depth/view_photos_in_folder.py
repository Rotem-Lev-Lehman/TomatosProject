import cv2
import os
from tqdm import tqdm


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] in ['.png', '.jpeg']]
    return files


def view_images(original_img_path, cropped_img_path):
    original_img = cv2.imread(original_img_path)
    cropped_img = cv2.imread(cropped_img_path)
    cv2.imshow("original", original_img)
    cv2.imshow("cropped", cropped_img)
    cv2.waitKey(0)


main_folder_path = r'C:\Users\User\Desktop\second_degree\tomatos_project\Progress\New_Data\guy'
original_images_path = fr'{main_folder_path}\images'
cropped_images_path = fr'{main_folder_path}\Cut_images'
original_images_names = get_all_files(original_images_path)

for img_path in tqdm(original_images_names):
    filename = os.path.basename(img_path)
    cropped_img_folder_name = filename.split('.')[0]
    cropped_img_path = fr'{cropped_images_path}\{cropped_img_folder_name}\bgr_image.png'
    print(f'Current img name: {cropped_img_folder_name}')
    view_images(img_path, cropped_img_path)
