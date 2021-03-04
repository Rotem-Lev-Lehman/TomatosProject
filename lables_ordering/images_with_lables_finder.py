from distutils.dir_util import copy_tree
import pandas as pd
from tqdm import tqdm

all_images_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data\All_cut_images"
only_labeled_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Data\Only_labeled_images"
labels_file_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\Labeled-TYLV\rating.csv"

labels = pd.read_csv(labels_file_path)
for index, row in tqdm(labels.iterrows()):
    img_full_name = row['image']
    rating = row['rating']

    img_name = img_full_name.split('_zssr_')[0]
    src_dir_path = fr"{all_images_path}\{img_name}"
    dest_dir_path = fr"{only_labeled_path}\{img_name}"
    copy_tree(src_dir_path, dest_dir_path)
