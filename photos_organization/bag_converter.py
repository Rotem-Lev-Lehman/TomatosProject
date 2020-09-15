import pyrealsense2 as rs
import numpy as np
import cv2

import os
global dis_filter
global dec_filter
global temp_filter
global spat_filter
global fill_hole_filter
from os import listdir
from os.path import isfile, join
def post_processing(flag):
    global dis_filter
    global dec_filter
    global temp_filter
    global spat_filter
    global fill_hole_filter

    temp_filter.set_option(rs.option.filter_smooth_alpha, 0.4)
    temp_filter.set_option(rs.option.filter_smooth_delta, 20)
    temp_filter.set_option(rs.option.holes_fill, 0)
    spat_filter.set_option(rs.option.filter_smooth_alpha,0.5)
    spat_filter.set_option(rs.option.filter_smooth_delta,20)
    spat_filter.set_option(rs.option.filter_magnitude, 3)
    spat_filter.set_option(rs.option.holes_fill,1)
    #dec_filter.set_option(rs.option.filter_magnitude, 2)
    if flag==True:
        fill_hole_filter.set_option(rs.option.holes_fill, 1)


def read_bag(file_name,bag_path,save_path,frame_number,flag=False):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    global dis_filter
    global dec_filter
    global temp_filter
    global spat_filter
    global fill_hole_filter

    bag_name = file_name.split('.')[0]
    config = rs.config()
    rs.config.enable_device_from_file(config,bag_path)
    pipeline = rs.pipeline()
    config.enable_all_streams()
    pipeline.start(config)
    dis_filter = rs.disparity_transform(False)
    temp_filter = rs.temporal_filter()
    spat_filter = rs.spatial_filter()
    fill_hole_filter = rs.hole_filling_filter()
    post_processing(flag)

    align_to = rs.stream.color
    align = rs.align(align_to)
    try:
        i=0
        while True:
            # start saving images from frame number 10
            # stop taking images from frame number 11
            if i>frame_number:
                break
            if (i==frame_number): # saving only the third frame
                frames  =  pipeline.wait_for_frames()
                aligned_frames = align.process(frames)
                depth = aligned_frames.get_depth_frame()
                color = aligned_frames.get_color_frame()
                #depth = dis_filter.process(depth)
                #depth = spat_filter.process(depth)
                #depth = temp_filter.process(depth)
                if flag==True:
                    depth = fill_hole_filter.process(depth)
                depth_image = np.asanyarray(depth.get_data())
                color_image = np.asanyarray(color.get_data())
                color_image = cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB)
                #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.07), cv2.COLORMAP_JET)
                depth_color_frame = rs.colorizer().colorize(depth)
                depth_colormap = np.asanyarray(depth_color_frame.get_data())
                cv2.imwrite(save_path+'\\'+str(bag_name)+'_'+"color_{}.png".format(i),color_image)
                cv2.imwrite(save_path+'\\'+str(bag_name)+'_'+"depth_{}.tiff".format(i),depth_image)
                cv2.imwrite(save_path+'\\'+str(bag_name)+'_'+"colormap_{}.tiff".format(i),depth_colormap)
                i+=1
            else:
                i+=1
    except Exception as ex:
            print (ex)


main_folder = r"C:\Users\User\Desktop\second_degree\tomatos_project\data\week2"
root = main_folder + r"\bags"  # bags files folder
save_path = main_folder + r"\images"  # path for saving images
frame_number = 0  # number of frame which will be saved
index = 0

for path, subdirs, files in os.walk(root):
    for name in files:
        bag_path = join(path, name)
        print(index, ":", bag_path)
        save_image_path = save_path + '\\' + name.replace(".bag", "")
        if not os.path.exists(save_image_path):
            os.makedirs(save_image_path)
        if len(os.listdir(save_image_path)) == 0:
            try:
                read_bag(name, join(path, name), save_image_path, frame_number)
            except:
                print('The bag file: ' + name + ' is corrupted, so ignoring it.')
        else:
            print("skipping this bag because it was already handled")
        index += 1
