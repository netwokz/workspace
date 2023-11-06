import tkinter as Tk
from PIL import Image, ImageTk
import random
import glob
import os

BASE_DIR_PATH = os.path.expanduser("~")


class GUI:
    last_5_filenames = []

    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.mainwin.title("Our Photos")
        self.mainwin.configure(bg="black")
        self.counter = 0

        self.frame = Tk.Frame(mainwin)
        self.frame.place(relx=0.5, rely=0.5, anchor=Tk.CENTER)

        self.img = Tk.Label(self.frame)
        self.img.pack()

        # directory = r"C:\Users\netwokz\Documents\CODE\workspace\python\photo_gallery\images"
        directory = BASE_DIR_PATH + "\CODE\workspace\python\photo_gallery\images"
        self.pic_list = glob.glob(f"{directory}/*")
        self.pic()

    def resize_image(self, img, img_height):
        hpercent = img_height / float(img.size[1])
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, img_height))
        return img

    def get_unique_image(self):
        filename = random.choice(self.pic_list)
        if filename in self.last_5_filenames:
            while filename in self.last_5_filenames:
                filename = random.choice(self.pic_list)
                return filename
        else:
            return filename

    def pic(self):
        # filename = random.choice(self.pic_list)
        filename = self.get_unique_image()
        print(filename)
        image = Image.open(filename)
        img_height = root.winfo_height()
        if img_height == 1:
            img_height = 500
        new_image = self.resize_image(image, img_height)
        self.photo = ImageTk.PhotoImage(new_image)
        self.img.config(image=self.photo)
        if len(self.last_5_filenames) < 3:
            print(len(self.last_5_filenames))
            print(f"{filename}")
            self.last_5_filenames.append(filename)
        else:
            for item in self.last_5_filenames:
                print(f"{item}")
            self.last_5_filenames.pop(0)
            self.last_5_filenames.append(filename)
        self.counter += 1

        if self.counter >= len(self.pic_list):
            self.counter = 0

        root.after(2000, self.pic)


root = Tk.Tk()
myprog = GUI(root)
root.geometry("1000x800")
root.mainloop()
