import os
from distutils.dir_util import copy_tree
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk

'''
def change_pic(path):
    root.photo = ImageTk.PhotoImage(Image.open(path))
    vlabel.configure(image=root.photo)
    print("updated")
'''


def show_image(path, folder_name):
    fig.set_tight_layout(True)
    plt.ion()
    image_path = os.path.join(path, folder_name + "_color_0.png")

    '''
    change_pic(image_path)
    root.mainloop()
    '''
    image = mpimg.imread(image_path)
    ax = fig.add_subplot(1, 1, 1)
    imgplot = plt.imshow(image)
    plt.show(block=False)

    print("showing photo", folder_name)
    while True:
        choice = input('Choose what to do with this photo:\n'
                            '\tk = keep at the same folder as the previous photo.\n'
                            '\ts = put at a new sign folder at the same row.\n'
                            '\tr = put at a new row folder which will contain a new sign folder in it.\n'
                            'place your choice please: ')
        if choice == "k":
            print("You have chosen to put the photo at the same folder as the previous photo.")
            break
        elif choice == "s":
            print("You have chosen to put the photo in a new sign folder at the same row.")
            break
        elif choice == "r":
            print("You have chosen to put the photo in a new row folder.")
            break
        else:
            print("You need to enter input from the menu only. Please try again.")
    plt.clf()
    plt.close(fig)

    return choice

'''
def next_photo():
    print("going to next photo")
'''


def organize_photos(photos_folder, dest_folder):
    # def organize_photos():
    print("Starting to organize photos into different rows of tomatoes")
    tomatoes_row_index = 0
    sign_index = 0
    for subdir, dirs, files in os.walk(photos_folder):
        for folder in dirs:
            path = os.path.join(subdir, folder)
            choice = show_image(path, folder)
            if choice == "s":
                print("creating a new folder for the new sign")
                sign_index += 1
            elif choice == "r":
                print("creating a new folder for the new row")
                tomatoes_row_index += 1
                sign_index = 0
            dest_path = os.path.join(dest_folder, "row_" + str(tomatoes_row_index), "sign_" + str(sign_index), folder)
            copy_tree(path, dest_path)
            print("copied this photo into row number", tomatoes_row_index, "and sign number", sign_index)
            print()




fig = plt.figure()


#root = tk.Tk()

#photo = r'C:\Users\User\coding\pythonProjects\TomatosProject\app_images\tomatoes_image.jpg'
#root.photo = ImageTk.PhotoImage(Image.open(photo))

#vlabel = tk.Label(root, image=root.photo)
#vlabel.pack()


photos_folder = r"C:\Users\User\Desktop\second_degree\tomatos_project\data\week1\images"
dest_folder = r"C:\Users\User\Desktop\second_degree\tomatos_project\organized\week1"
'''
b2 = tk.Button(root, text="Next photo", command=next_photo)
b2.pack()
'''

organize_photos(photos_folder, dest_folder)
