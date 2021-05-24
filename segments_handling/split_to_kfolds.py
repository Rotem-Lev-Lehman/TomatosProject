import os
from glob import glob
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

base_filepath = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress\May_stuff\segments"
train_files = fr'{base_filepath}\Segments\Train\*'
test_files = fr'{base_filepath}\Segments\Test\*'
imagePatches_train = glob(os.path.join(train_files, '**.jpg'), recursive=True)
imagePatches_test = glob(os.path.join(test_files, '**.jpg'), recursive=True)
all_image_paths = imagePatches_train + imagePatches_test

only_image_name = [os.path.basename(image_path) for image_path in all_image_paths]
only_image_class = [Path(image_path).parent.name for image_path in all_image_paths]
only_train_test_location = [Path(image_path).parent.parent.name for image_path in all_image_paths]

k = 5
out_csv_filepath = fr'{base_filepath}\fold_split_{k}.csv'


def get_original_image_name(image_name):
    split_image_name = image_name.split('_zssr_')
    return split_image_name[0]


original2cuts = {}
for image in only_image_name:
    original_image_name = get_original_image_name(image)
    if original_image_name not in original2cuts.keys():
        original2cuts[original_image_name] = []
    original2cuts[original_image_name].append(image)

original_images = np.array(list(original2cuts.keys()))

d = {'image': only_image_name,
     'class': only_image_class,
     'location': only_train_test_location}
df = pd.DataFrame(d)

kf = KFold(n_splits=k, shuffle=True, random_state=42)
for i, (train_index, test_index) in enumerate(kf.split(original_images)):
    original_train = original_images[train_index]

    train_images = [original2cuts[org] for org in original_train]
    train_images_flattened = set([item for sublist in train_images for item in sublist])
    df[f'fold_{i}'] = df['image'].apply(lambda name: name in train_images_flattened)

df.to_csv(out_csv_filepath)
