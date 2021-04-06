import cv2
import numpy as np
import os
from pathlib import Path
import gdal
from tqdm import tqdm
import pandas as pd

from itertools import product, repeat
import networkx as nx

main_path = r"C:\Users\User\Desktop\second_degree\tomatos_project\Progress"

original_images_path = fr"{main_path}\Data\All_cut_images"

output_cut_images_dir_path = fr"{main_path}\April_stuff\week3_cropped_with_depth"
csv_images_names = fr"{main_path}\April_stuff\week3_guy_shani.txt"
Path(output_cut_images_dir_path).mkdir(parents=True, exist_ok=True)


def get_nx_indices_graph(img_shape):
    # generate edges
    shift = list(product(*repeat([-1, 0, 1], 2)))
    x_max, y_max = img_shape
    edges = []

    for x, y in np.ndindex(img_shape):
        for x_delta, y_delta in shift:
            x_neighb = x + x_delta
            y_neighb = y + y_delta
            if (0 <= x_neighb < x_max) and (0 <= y_neighb < y_max):
                edge = (x, y), (x_neighb, y_neighb)
                edges.append(edge)

    # build graph
    G = nx.from_edgelist(edges)

    # draw graph
    #pos = {(x, y): (y, x_max - x) for x, y in G.nodes()}
    #nx.draw(G, with_labels=True, pos=pos, node_color='coral', node_size=1000)

    return G


def find_end_of_group(depth_x_array, from_point, to_point, steps, group_val):
    prev = from_point
    for x in range(from_point, to_point, steps):
        if depth_x_array[x] != group_val:
            return prev
        prev = x
    return prev


def find_start_and_end_of_group(depth_x_array, point, group_val):
    start = find_end_of_group(depth_x_array, from_point=point, to_point=-1, steps=-1, group_val=group_val)
    end = find_end_of_group(depth_x_array, from_point=point, to_point=len(depth_x_array), steps=1, group_val=group_val)
    return start, end


def find_central_group(depth_x_array, group_val=1):
    center = int(len(depth_x_array) / 2)
    if depth_x_array[center] == group_val:
        return find_start_and_end_of_group(depth_x_array, center, group_val)
    for i in range(int(len(depth_x_array) / 2)):
        curr_left_ind = center - i
        if depth_x_array[curr_left_ind] == group_val:
            return find_start_and_end_of_group(depth_x_array, curr_left_ind, group_val)
        curr_right_ind = center + i
        if depth_x_array[curr_right_ind] == group_val:
            return find_start_and_end_of_group(depth_x_array, curr_right_ind, group_val)
    # can not get here...
    raise Exception('There is no one in the group... Something is wrong here...')


def find_closest_to_camera(rgb_img, depth_img, percentile):
    # percentile = 10
    percentile_val = np.percentile(depth_img[depth_img != 0], percentile)
    range_indices = np.logical_not(np.logical_or(depth_img > percentile_val, depth_img == 0))

    depth_mask_image = np.zeros(rgb_img.shape[:-1])
    depth_mask_image[range_indices] = 1
    depth_x_array = np.zeros(rgb_img.shape[1])
    indices = np.argwhere(depth_mask_image)

    for col in range(len(depth_x_array)):
        depth_x_array[col] = 1 if 1 in depth_mask_image[:, col] else 0

    # find the most central group (x-wise):
    x_start, x_end = find_central_group(depth_x_array)
    group_indices = np.array([[y, x] for y, x in indices if x_start <= x <= x_end])
    cropped_rgb_img, cropped_depth_img = crop_by_indices(rgb_img, depth_img, group_indices)
    # depth_mask_only_group = np.zeros(depth_mask_image.shape)
    # depth_mask_only_group[tuple(group_indices.T)] = 1
    #
    # in_range_indices = np.where(depth_mask_only_group == 1)
    # min_x = int(np.min(in_range_indices[0]) * 0.9)
    # max_x = int(np.max(in_range_indices[0]) * 1.1)
    # min_y = int(np.min(in_range_indices[1]) * 0.9)
    # max_y = int(np.max(in_range_indices[1]) * 1.1)
    #
    # cropped_rgb_img = rgb_img[min_x:max_x, min_y: max_y]
    # cropped_depth_img = depth_img[min_x:max_x, min_y: max_y]

    # depth_mask_image = depth_mask_image * 255
    # depth_mask_only_group = depth_mask_only_group * 255

    # cv2.imwrite('Depth_10_percentage_selection.png', depth_mask_image)
    # cv2.imwrite('Depth_selected_group.png', depth_mask_only_group)
    # cv2.imwrite('RGB_cropped_central_group.png', cropped_rgb_img)
    # cv2.imwrite('RGB_before_crop.png', rgb_img)

    # cv2.imshow("x_array", depth_x_array)
    # cv2.imshow("rgb image", rgb_img)
    # cv2.imshow("depth_rgb_image", depth_mask_image)
    # cv2.imshow("depth_rgb_image - central group only", depth_mask_only_group)
    #
    # cv2.waitKey(0)

    # G = get_nx_indices_graph(depth_mask_image.shape)
    # print("Created graph")
    # G_curr = G.subgraph(map(tuple, select))
    # print("Created sub-graph")
    # components = nx.connected_components(G_curr)
    # print("Created connected components")
    #
    # # find connected components and DFS trees
    # for i in components:
    #     source = next(iter(i))
    #     idx = nx.dfs_tree(G_curr, source=source)
    #     print(tuple(np.array(idx).T))

    # cv2.imshow("rgb image", rgb_img)
    #depth_marked_img = rgb_img
    #depth_marked_img[np.logical_not(range_indices)] = (255, 0, 0)
    # cv2.imshow("depth_rgb_image", depth_mask_image)
    # cv2.waitKey(0)

    return cropped_rgb_img, cropped_depth_img


def crop_by_indices(rgb_img, depth_img, indices):
    depth_mask = np.zeros(rgb_img.shape[:-1])
    depth_mask[tuple(indices.T)] = 1

    in_range_indices = np.where(depth_mask == 1)
    min_x = int(np.min(in_range_indices[0]) * 0.9)
    max_x = int(np.max(in_range_indices[0]) * 1.1)
    min_y = int(np.min(in_range_indices[1]) * 0.9)
    max_y = int(np.max(in_range_indices[1]) * 1.1)

    cropped_rgb_img = rgb_img[min_x:max_x, min_y: max_y]
    cropped_depth_img = depth_img[min_x:max_x, min_y: max_y]
    return cropped_rgb_img, cropped_depth_img


def crop_plant(rgb_img, depth_img, percentile):
    percentile_val = np.percentile(depth_img[depth_img != 0], percentile)
    range_indices = np.logical_not(np.logical_or(depth_img > percentile_val, depth_img == 0))
    depth_mask_image = np.zeros(rgb_img.shape[:-1])
    depth_mask_image[range_indices] = 1
    indices = np.argwhere(depth_mask_image)
    return crop_by_indices(rgb_img, depth_img, indices)


def find_and_save_cuts(rgb_image_path, depth_image_path, img_files_base_path, percentile, cut_whole_image=True):
    rgb_img = cv2.imread(rgb_image_path)
    depth_img = gdal.Open(depth_image_path).ReadAsArray()

    if cut_whole_image:
        cropped_rgb_img, cropped_depth_img = find_closest_to_camera(rgb_img, depth_img, percentile)
    else:
        cropped_rgb_img, cropped_depth_img = crop_plant(rgb_img, depth_img, percentile)

    Path(img_files_base_path).mkdir(parents=True, exist_ok=True)

    bgr_img_out_path = fr"{img_files_base_path}\bgr_image.png"
    depth_img_out_path = fr"{img_files_base_path}\depth_image.png"
    depth_tiff_out_path = fr"{img_files_base_path}\tiff_depth_image.tiff"

    cv2.imwrite(bgr_img_out_path, cropped_rgb_img)
    cv2.imwrite(depth_img_out_path, cropped_depth_img)
    cv2.imwrite(depth_tiff_out_path, cropped_depth_img)


def get_all_files(directory_path):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory_path) for f in filenames if os.path.splitext(f)[1] in ['.png', '.jpeg']]
    return files


df_filenames = pd.read_csv(csv_images_names, header=None)
filenames = df_filenames[1]
images_names = list(filenames.apply(lambda x: x.split('_zssr')[0]))

for img_name in tqdm(images_names):
    original_path = fr'{original_images_path}\{img_name}'
    output_path = fr'{output_cut_images_dir_path}\{img_name}'

    rgb_img_path = fr'{original_path}\bgr_image.png'
    depth_img_path = fr'{original_path}\tiff_depth_image.tiff'

    find_and_save_cuts(rgb_img_path, depth_img_path, output_path, percentile=10, cut_whole_image=False)


print('Done!')
# original_images_names = get_all_files(original_images_path)
#
# for img_path in tqdm(original_images_names):
#     filename = os.path.basename(img_path)
#     cut_img_name = filename.split('.')[0]
#     img_name = cut_img_name.split('_color_0')[0] + '_color_0'
#     depth_image_path = img_path.split('_color_0')[0] + '_depth_0.tiff'
#     img_files_base_path = fr"{output_cut_images_dir_path}\{img_name}"
#     fix the function call:
#     find_and_save_cuts(img_path, depth_image_path, , percentile=10, cut_whole_image=True)
