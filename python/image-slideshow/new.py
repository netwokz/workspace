import tkinter as tk
from PIL import ImageTk, Image
import random
import os
import re

img_directory = "C:\\Users\\netwokz\\Desktop\\photos-renamed"

root = tk.Tk()
root.attributes('-fullscreen', 1)  # make the root window fullscreen
root.config(cursor="none")  # hide the mouse cursor

image_list = []
# old_images = []
# photos = []
color_list = []


def showPIL(pilImage):
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize(
            (imgWidth, imgHeight), Image.Resampling.LANCZOS)
    pilImage = ImageTk.PhotoImage(pilImage)
    root.mainloop()


def get_photos():
    for (root_, dirs, files) in os.walk(img_directory):
        for file_ in files:
            path = os.path.join(img_directory, file_)
            image_list.append(path)
    image_list.sort(key=natural_keys)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


get_photos()


def newPicture():
    random_filename = random.choice(image_list)
    pilImage = Image.open(random_filename)
    showPIL(pilImage)


def getNextColor():
    color = random.choice(color_list)
    return color


def slideShow():
    displayCanvas.config(image=newPicture())
    root.after(2000, slideShow)


displayCanvas = tk.Label(root)
displayCanvas.pack(expand=1, fill=tk.BOTH)

# allow Esc key to terminate the slide show
root.bind('<Escape>', lambda e: root.destroy())
slideShow()  # start the slide show

# root.focus_force()
root.mainloop()
