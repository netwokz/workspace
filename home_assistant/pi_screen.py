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
        load_dotenv(dotenv_path=os.path.expanduser("~\\Documents\\CODE\\workspace\\home_assistant\\.env"))
        HA_API_TOKEN = os.getenv("HA_API_TOKEN")

        # Load credentials
        self.headers = {
            "Authorization": f"Bearer {HA_API_TOKEN}",
            "content-type": "application/json",
        }

        WIDTH = 1024
        HEIGHT = 600

        self.desk_default_color = "#ff0000"
        self.kitchen_under_cabinet_led_default_color = "#546E7A"

        self.desk_wled_color = "#ff0000"
        self.kitchen_lower_wled_color = "#546E7A"

        # configure the root window
        self.title("Simpile Monitor") 
        self.resizable(0, 0)
        self.geometry("1024x600")
        self["bg"] = "#26242f"

        # Desk LED Light
        self.desk_light_widget = Frame(master=self, width=300, height=125, bg=self.desk_default_color, relief=RAISED, borderwidth=5)
        self.desk_light_widget_label = Label(self.desk_light_widget, text="Desk WLED")
        # self.desk_light_widget.bind("<Button-1>", lambda e: self.update_desk())
        self.desk_light_widget.place(x=0, y=0)
        self.desk_light_widget_label.place(x=10, y=0)

        # Kitchen Overhead Light
        self.kitchen_light_widget = Frame(master=self, width=300, height=125, bg="#ff0000", relief=RAISED, borderwidth=5)
        # # self.kitchen_light.bind("<Button-1>", lambda e: button_function())
        self.kitchen_light_widget.place(x=532, y=264)

        self.kitchen_under_cabinet_led = Frame(master=self, width=300, height=125, bg=self.kitchen_under_cabinet_led_default_color, relief=RAISED, borderwidth=5)
        # self.kitchen_under_counter_led.bind("<Button-1>", lambda e: self.update_desk())
        self.kitchen_under_cabinet_led.place(x=WIDTH - 300, y=HEIGHT - 125)

        # self.label = ttk.Label(self, text=self.time_string())
        # self.label.place(x=1024 / 2, y=(600 - 20))

        self.after(500, self.refresh_data)

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
        self.desk_light_widget.configure(bg=self.desk_wled_color)
        self.kitchen_under_cabinet_led.configure(bg=self.kitchen_lower_wled_color)

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
                    self.desk_wled_color = self.rgb_to_hex(*temp_color)

                    # print(state["attributes"]["effect"])
                    # print(state["attributes"]["brightness"])
                else:
                    self.desk_wled_color = self.desk_default_color

            if state["entity_id"] == "switch.kitchen_light":
                # print(f"Kitchn Light is {state['state']}")
                pass

            if state["entity_id"] == "kitchen_under_cabinet_led_2":
                if state["state"] == "on":
                    temp_color = state["attributes"]["rgb_color"]
                    self.kitchen_lower_wled_color = self.rgb_to_hex(*temp_color)
                    # print(state["attributes"]["effect"])
                    # print(state["attributes"]["brightness"])
                else:
                    # global wled_color
                    self.kitchen_lower_wled_color = self.kitchen_under_cabinet_led_default_color
        self.update_gui()
        self.after(1000, self.refresh_data)


if __name__ == "__main__":
    clock = SimMon()
    clock.mainloop()
