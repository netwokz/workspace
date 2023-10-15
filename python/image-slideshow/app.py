from hashlib import new
from importlib.resources import path
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
import time
import random

folder = "images"

# Setup main window
# root_window = tk.Tk()
# root_window.geometry("1280x720")

# Load the Images
images = []
for (root_, dirs, files) in os.walk(folder):
    if files:
        for file_ in files:
            path = os.path.join(folder, file_)
            image_ = Image.open(path)
            images.append(image_)


def showPIL(pilImage):
    root_window = tk.Tk()
    w, h = root_window.winfo_screenwidth(), root_window.winfo_screenheight()
    root_window.overrideredirect(1)
    root_window.geometry("%dx%d+0+0" % (w, h))
    root_window.focus_set()
    root_window.bind("<Escape>", lambda e: (
        e.widget.withdraw(), e.widget.quit()))
    canvas = tk.Canvas(root_window, width=w, height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize(
            (imgWidth, imgHeight), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(pilImage)
    canvas.delete()
    canvas.create_image(w/2, h/2, image=image)
    root_window.mainloop()


def newPicture():
    random_filename = random.choice([
        x for x in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, x))
    ])
    pilImage = Image.open(f'{folder}\{random_filename}')
    print(pilImage)
    showPIL(pilImage)
    print(random_filename)


count = 0
while (count < 10):
    count += 1
    newPicture()
    time.sleep(2)
