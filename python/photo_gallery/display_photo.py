import tkinter as Tk
from PIL import Image, ImageTk
import random
import glob


class GUI:
    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.mainwin.title("Our Photos")
        self.mainwin.configure(bg="grey")
        self.counter = 0

        self.frame = Tk.Frame(mainwin)
        self.frame.place(relheight=0.99, relwidth=0.99, relx=0.05, rely=0.05)

        self.img = Tk.Label(self.frame)
        self.img.pack()

        directory = r"C:\Users\netwokz\Documents\CODE\workspace\python\photo_gallery\images"
        self.pic_list = glob.glob(f"{directory}/*")
        self.colours = [
            "snow",
            "ghost white",
            "white smoke",
            "gainsboro",
            "floral white",
            "old lace",
            "linen",
            "antique white",
            "papaya whip",
            "blanched almond",
            "bisque",
            "peach puff",
            "navajo white",
            "lemon chiffon",
        ]

        # self.colour()
        self.pic()

    def colour(self):
        selected = random.choice(self.colours)
        self.mainwin.configure(bg=selected)
        self.frame.configure(bg="grey")
        root.after(4000, self.colour)

    def resize_image(self, img, img_height):
        hpercent = img_height / float(img.size[1])
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, img_height), Image.ANTIALIAS)
        return img

    def pic(self):
        filename = self.pic_list[self.counter]
        image = Image.open(filename)
        img_height = root.winfo_height()
        print(f"Width: {root.winfo_width()}")
        print(f"Height: {root.winfo_height()}")
        if root.winfo_height() == 1:
            img_height = 500
        new_image = self.resize_image(image, img_height)
        self.photo = ImageTk.PhotoImage(new_image)
        self.img.config(image=self.photo)

        self.counter += 1

        if self.counter >= len(self.pic_list):
            self.counter = 0

        root.after(2000, self.pic)


root = Tk.Tk()
myprog = GUI(root)
root.geometry("1000x1000")
root.mainloop()
