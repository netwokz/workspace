import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
import random
from random import randint
import os
import re

img_directory = "C:\\Users\\netwokz\\Desktop\\photos-renamed"
root = tk.Tk()
# root.attributes('-fullscreen', 1)  # make the root window fullscreen
root.config(cursor="none")  # hide the mouse cursor

image_list = []

new_images = []
old_images = []
photos = []
color_list = []

# get the screen size
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()

for image in new_images:
    img = Image.open(image)
    photos.append(img)

for i in range(100):
    color = '#%06X' % randint(0, 0xFFFFFF)
    if color not in color_list:
        color_list.append(color)


def getNextPhoto():
    while True:
        img = Image.open(random.choice(image_list))
        if img.filename not in old_images:
            if len(old_images) < 10:
                old_images.append(img.filename)
                if img.width > scr_width or img.height > scr_height:
                    # only resize image bigger than the screen
                    ratio = min(scr_width/img.width, scr_height/img.height)
                    img = img.resize(
                        (int(img.width*ratio), int(img.height*ratio)))
                    photo = ImageTk.PhotoImage(img)
                    return photo
                photo = ImageTk.PhotoImage(img)
                return photo
            else:
                old_images.pop(0)
                old_images.append(img.filename)
                if img.width > scr_width or img.height > scr_height:
                    # only resize image bigger than the screen
                    ratio = min(scr_width/img.width, scr_height/img.height)
                    img = img.resize(
                        (int(img.width*ratio), int(img.height*ratio)))
                    photo = ImageTk.PhotoImage(img)
                    return photo
                photo = ImageTk.PhotoImage(img)
                return photo


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def get_photos():
    for (root_, dirs, files) in os.walk(img_directory):
        for file_ in files:
            path = os.path.join(img_directory, file_)
            image_list.append(path)
    image_list.sort(key=natural_keys)


def getNextColor():
    color = random.choice(color_list)
    return color


def slideShow():
    displayCanvas.config(image=getNextPhoto(), background=getNextColor())
    root.after(2000, slideShow)


get_photos()

displayCanvas = tk.Label(root)
displayCanvas.pack(expand=1, fill=tk.BOTH)

# allow Esc key to terminate the slide show
root.bind('<Escape>', lambda e: root.destroy())
slideShow()  # start the slide show

root.focus_force()
root.mainloop()
