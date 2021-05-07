from pathlib import Path
import xmltodict
import os
from tqdm import tqdm
import cv2
import csv
import random


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] == '.xml']
    return files


base_folder_path = r'C:\Users\User\Desktop\second_degree\tomatos_project\Progress\April_stuff\Leaf_taggings'
annotation_files_directory = fr'{base_folder_path}\annotations'
original_plants_directory = fr'{base_folder_path}\tags_100_each'

output_cropped_leafs_directory = fr'{base_folder_path}\cropped_leafs'
Path(output_cropped_leafs_directory).mkdir(parents=True, exist_ok=True)
output_leaf_tags_file = fr'{base_folder_path}\leafs_tags.csv'
tags = {}

all_xml_files = get_all_files(base_folder_path)


def read_image(image_name, directory):
    full_image_path = fr'{directory}\{image_name}'
    image_data = cv2.imread(full_image_path)
    return image_data


def get_data_from_leaf_dict(leaf_dict):
    xtl = int(float(leaf_dict['@xtl']))
    ytl = int(float(leaf_dict['@ytl']))
    xbr = int(float(leaf_dict['@xbr']))
    ybr = int(float(leaf_dict['@ybr']))
    label = leaf_dict['@label']
    return xtl, ytl, xbr, ybr, label


def crop_and_save_leaf(image_data, leaf_dict, image_name, tags, output_cropped_leafs_directory):
    xtl, ytl, xbr, ybr, label = get_data_from_leaf_dict(leaf_dict)

    img_show = cv2.resize(image_data, (500, 500))
    cv2.rectangle(image_data, (int(xtl), int(ytl)), (int(xbr), int(ybr)), random_color(), 2)
    original_image_resized = cv2.resize(image_data, (500, 500))
    cv2.imshow('original_image', original_image_resized)

    height_diff = image_data.shape[0] / 500
    width_diff = image_data.shape[1] / 500
    xtl /= width_diff
    xbr /= width_diff
    ytl /= height_diff
    ybr /= height_diff
    cv2.rectangle(img_show, (int(xtl), int(ytl)), (int(xbr), int(ybr)), random_color(), 1)
    cv2.imshow('resized_image', img_show)
    cv2.waitKey(0)

    #
    # cropped_image = image_data[ytl:ybr, xtl:xbr]
    # leaf_image_name = f'{image_name}_leaf_{xtl}_{ytl}_{xbr}_{ybr}.png'
    # if leaf_image_name in tags.keys():
    #     raise Exception('Same leaf tagged twice...')
    # tags[leaf_image_name] = label
    # saving_file_path = fr'{output_cropped_leafs_directory}\{leaf_image_name}'
    # cv2.imwrite(saving_file_path, cropped_image)


def get_name_for_leafs(name):
    return name.split('/')[1].split('.jpg')[0]


def write_tags_to_csv_file(tags, output_leaf_tags_file):
    items = [(k, v) for k, v in tags.items()]
    with open(output_leaf_tags_file, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['image', 'tag'])
        csv_out.writerows(items)


for xml_file in all_xml_files:
    print(f'Reading file {xml_file}')
    with open(xml_file, 'r') as file:
        xml_data = file.read()
        data = xmltodict.parse(xml_data)
        images = data['annotations']['image']
        for image_dict in tqdm(images):
            name = image_dict['@name']
            image_data = read_image(name, original_plants_directory)

            image_name_for_leafs = get_name_for_leafs(name)
            if 'box' in image_dict:  # check if this image was tagged
                leafs = image_dict['box']
                if not isinstance(leafs, list):  # only one tag in this image
                    leafs = [leafs]
                for leaf_dict in leafs:
                    crop_and_save_leaf(image_data, leaf_dict, image_name_for_leafs, tags, output_cropped_leafs_directory)

write_tags_to_csv_file(tags, output_leaf_tags_file)
