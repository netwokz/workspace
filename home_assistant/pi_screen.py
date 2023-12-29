import json
import os
import time
from textwrap import fill
from tkinter import *
from turtle import bgcolor

from dotenv import load_dotenv
from requests import get, post


class SimMon(Tk):
    def __init__(self):
        super().__init__()

        # Load credentials
        load_dotenv(dotenv_path=os.path.expanduser("~\\Documents\\CODE\\workspace\\\home_assistant\\.env"))
        HA_API_TOKEN = os.getenv("HA_API_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {HA_API_TOKEN}",
            "content-type": "application/json",
        }

        self.wled_color = "#AEAEAE"

        WIDTH = 1024
        HEIGHT = 600

        # configure the root window
        self.title("Simpile Monitor")
        self.resizable(0, 0)
        self.geometry("1024x600")
        self["bg"] = "#26242f"

        self.desk_light_widget = Frame(master=self, width=300, height=125, bg="#ff0000", relief=RAISED, borderwidth=5)
        self.desk_light_widget_label = Label(self.desk_light_widget, text="Desk WLED")
        self.desk_light_widget.bind("<Button-1>", lambda e: self.update_desk())
        # self.desk_light_widget_label.pack()
        # self.desk_light_widget.pack()

        self.kitchen_light_widget = Frame(master=self, width=300, height=125, bg="#ff0000", relief=RAISED, borderwidth=5)
        # # self.kitchen_light.bind("<Button-1>", lambda e: button_function())

        # self.label = ttk.Label(self, text=self.time_string())
        # self.label.place(x=1024 / 2, y=(600 - 20))

        # schedule an update every 1 second
        self.kitchen_light_widget.place(x=532, y=264)

        self.desk_light_widget.place(x=0, y=0)
        self.desk_light_widget_label.place(x=10, y=0)

        self.after(3000, self.refresh_data)

    def time_string(self):
        return time.strftime("%H:%M:%S")

    def hex_to_rgb(self, value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip("#")
        lv = len(value)
        return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgb_to_hex(self, red, green, blue):
        """Return color as #rrggbb for the given color values."""
        return "#%02x%02x%02x" % (red, green, blue)

    def update_gui(self):
        self.desk_light_widget.configure(bg=self.wled_color)

    def update_desk(self):
        pass

    def refresh_data(self):
        """update the data every 3 seconds"""
        # self.label.configure(text=self.time_string())

        response = get("http://10.10.10.7:8123/api/states", headers=self.headers).json()

        for state in response:
            if state["entity_id"] == "light.desk_rgb":
                if state["state"] == "on":
                    temp_color = state["attributes"]["rgb_color"]
                    self.wled_color = self.rgb_to_hex(*temp_color)

                    # print(state["attributes"]["effect"])
                    # print(state["attributes"]["brightness"])
                else:
                    # global wled_color
                    self.wled_color = "#2E9AFF"

            if state["entity_id"] == "switch.kitchen_light":
                # print(f"Kitchn Light is {state['state']}")
                pass
        self.update_gui()
        self.after(3000, self.refresh_data)


if __name__ == "__main__":
    clock = SimMon()
    clock.mainloop()
