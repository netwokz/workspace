import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
import random
from random import randint
import os
import time

folder = "C:\\Users\\netwokz\\Desktop\\photos-renamed"

root = tk.Tk()
root.attributes('-fullscreen', 1)  # make the root window fullscreen
root.config(cursor="none")  # hide the mouse cursor

new_images = []
old_images = []
color_list = []

for (root_, dirs, files) in os.walk(folder):
    if files:
        for file_ in files:
            path = os.path.join(folder, file_)
            img = Image.open(path)
            new_images.append(img)

# get the screen size
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()

# print("Preparing images ...")
photos = []
for img in new_images:
    if img.width > scr_width or img.height > scr_height:
        # only resize image bigger than the screen
        ratio = min(scr_width/img.width, scr_height/img.height)
        img = img.resize((int(img.width*ratio), int(img.height*ratio)))
    photos.append(ImageTk.PhotoImage(img))

for i in range(100):
    color = '#%06X' % randint(0, 0xFFFFFF)
    if color not in color_list:
        color_list.append(color)


def getNextPhoto():
    image = random.choice(photos)
    return image


def getNextColor():
    color = random.choice(color_list)
    return color


def slideShow():
    displayCanvas.config(image=getNextPhoto(), background=getNextColor())
    root.after(2000, slideShow)


displayCanvas = tk.Label(root)
displayCanvas.pack(expand=1, fill=tk.BOTH)

# allow Esc key to terminate the slide show
root.bind('<Escape>', lambda e: root.destroy())
slideShow()  # start the slide show

root.focus_force()
root.mainloop()
