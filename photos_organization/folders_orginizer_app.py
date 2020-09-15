import os
from distutils.dir_util import copy_tree
from tkinter import *

from PIL import Image, ImageTk


class MyWindow:
    def __init__(self, win):
        self.pixels_x = 1280
        self.pixels_y = 720

        self.lbl_photos_folder=Label(win, text='Photos folder')
        self.lbl_dest_folder=Label(win, text='Destination folder')
        self.t_photos=Entry()
        self.t_dest=Entry()
        self.btn_start = Button(win, text='Start organizing photos', command=self.start_organizing)
        self.btn_keep=Button(win, text='Keep in the same folder', command=self.keep)
        self.btn_new_row=Button(win, text='Put in a new tomatoes row', command=self.new_row)
        self.btn_new_sign=Button(win, text='Put in a new sign folder', command=self.new_sign)
        self.btn_skip=Button(win, text='Skip', command=self.skip)
        self.lbl_photos_folder.place(x=self.pixels_x + 25, y=100)
        self.t_photos.place(x=self.pixels_x + 125, y=100)
        self.lbl_dest_folder.place(x=self.pixels_x + 25, y=150)
        self.t_dest.place(x=self.pixels_x + 125, y=150)
        self.btn_start.place(x=self.pixels_x + 25, y=50)
        self.btn_keep.place(x=self.pixels_x + 25, y=200)
        self.btn_new_row.place(x=self.pixels_x + 25, y=300)
        self.btn_new_sign.place(x=self.pixels_x + 25, y=250)
        self.btn_skip.place(x=self.pixels_x + 25, y=350)
        # self.lbl3.place(x=100, y=200)
        # self.t3.place(x=200, y=200)
        self.tomatoes_row_index = 0
        self.sign_index = 0
        self.photos_folder = None
        self.dest_folder = None
        self.photos_generator = None
        self.current_folder = None
        self.current_path = None

        photo = r'..\app_images\tomatoes_image.jpg'
        self.photo = ImageTk.PhotoImage(Image.open(photo).resize((self.pixels_x, self.pixels_y)))

        self.vlabel = Label(win, image=self.photo)
        self.vlabel.place(x=10, y=10)

    def start_organizing(self):
        self.tomatoes_row_index = 0
        self.sign_index = 0
        self.photos_folder = self.t_photos.get()
        self.dest_folder = self.t_dest.get()
        self.photos_generator = self.photos_generator_func()
        self.continue_execution()

    def continue_execution(self):
        path, folder = next(self.photos_generator)
        if (path, folder) == (None, None):
            print("Finished all photos, stopping execution")
            exit(0)
        self.current_folder = folder
        self.current_path = path
        self.show_image()

    def keep(self):
        self.save_photo_in_new_dest()
        self.continue_execution()

    def skip(self):
        print("Skipping this photo")
        self.continue_execution()

    def new_row(self):
        print("creating a new folder for the new row")
        self.tomatoes_row_index += 1
        self.sign_index = 0
        self.save_photo_in_new_dest()
        self.continue_execution()

    def new_sign(self):
        print("creating a new folder for the new sign")
        self.sign_index += 1
        self.save_photo_in_new_dest()
        self.continue_execution()

    def save_photo_in_new_dest(self):
        dest_path = os.path.join(self.dest_folder, "row_" + str(self.tomatoes_row_index),
                                 "sign_" + str(self.sign_index), self.current_folder)
        copy_tree(self.current_path, dest_path)
        print("copied this photo into row number", self.tomatoes_row_index, "and sign number", self.sign_index)
        print()

    def photos_generator_func(self):
        for subdir, dirs, files in os.walk(self.photos_folder):
            for folder in dirs:
                path = os.path.join(subdir, folder)
                yield path, folder

        # In order to say we are done, we return None at the end of the generator function:
        yield None, None

    def show_image(self):
        image_path = os.path.join(self.current_path, self.current_folder + "_color_0.png")

        self.photo = ImageTk.PhotoImage(Image.open(image_path).resize((self.pixels_x, self.pixels_y)))
        self.vlabel.configure(image=self.photo)
        print("updated")
        print("showing photo", self.current_folder)


window = Tk()
mywin = MyWindow(window)
window.title('Organize folders')
pad = 3
window.geometry("{0}x{1}+0+0".format(
            window.winfo_screenwidth()-pad, window.winfo_screenheight()-pad))
window.mainloop()
