import json as js
from requests import post, get
import os
from dotenv import load_dotenv

load_dotenv()
ON = "on"
OFF = "off"

URL = "http://10.10.10.7:8123/api/states/light.wled"
token_path = os.path.expanduser("~\\Documents\\CODE\\workspace\\home_assistant\\")
load_dotenv(dotenv_path=token_path)
TOKEN = os.getenv("TOKEN")
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
}


def get_wled_status():
    response = get("http://10.10.10.7:8123/api/states", headers=headers).json()
    for state in response:
        if state["entity_id"] == "light.desk_rgb":
            print(state["state"])
            print(state["attributes"]["rgb_color"])
            print(state["attributes"]["effect"])
            print(state["attributes"]["brightness"])


get_wled_status()


def wled_on(brightness=76, color=[255, 0, 0]):
    URL = "http://homeassistant.computeerror.com:8123/api/services/light/turn_on"
    data = {"entity_id": "light.wled", "rgb_color": color, "brightness": brightness}
    response = post(URL, headers=headers, json=data)
    # print(response.status_code)


def wled_off():
    URL = "http://10.10.10.7:8123/api/services/light/turn_off"
    data = {"entity_id": "switch.kitchen_light"}
    response = post(URL, headers=headers, json=data)


# set_wled_status("off")

wled_on(60, [172, 164, 97])
