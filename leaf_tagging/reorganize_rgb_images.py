from shutil import copyfile
from tqdm import tqdm
import pandas as pd
from pathlib import Path

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\April_stuff"

original_images_path = fr"{main_path}\super_resolution_all_images"
organized_path = fr"{main_path}\super_resolution_chosen\tags_100_each"
Path(organized_path).mkdir(parents=True, exist_ok=True)

csv_images_names = fr"{main_path}\tagged_images_week3_and_4.txt"

df_filenames = pd.read_csv(csv_images_names, header=None)
for tag in range(5):  # 0 - 4
    print(f"Tag = {tag}")
    curr_tag_path = fr'{organized_path}\tag_{tag}'
    Path(curr_tag_path).mkdir(parents=True, exist_ok=True)
    curr_df = df_filenames[df_filenames[2] == tag]
    curr_filenames = list(curr_df[1])[:100]

    for file_name in tqdm(curr_filenames):
        original_rgb_img_path = fr'{original_images_path}\{file_name}'
        copy_img_path = fr'{curr_tag_path}\{file_name}'
        copyfile(original_rgb_img_path, copy_img_path)
