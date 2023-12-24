import requests
import pprint
import json

wled_basic = {
    "on": True,  # LED strip on/off
    "bri": 128,  # Brightness (0-255)
    "transition": 0,  # Transition time in seconds
    "mainseg": 0,
    "udpn": {"send": False, "recv": True},  # UDP notifications
    "seg": [{"start": 0, "stop": 85, "len": 85, "col": [[255, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], "fx": 0, "sx": 127, "ix": 127, "pal": 0, "sel": True, "rev": False, "cln": -1}],
}

wled_rainbow = {
    "on": True,
    "bri": 100,
    "transition": 7,
    "ps": -1,
    "pl": -1,
    "ccnf": {"min": 1, "max": 5, "time": 12},
    "nl": {"on": False, "dur": 60, "fade": True, "mode": 1, "tbri": 0, "rem": -1},
    "udpn": {"send": False, "recv": True},
    "lor": 0,
    "mainseg": 0,
    "seg": [
        {
            "id": 0,
            "start": 0,
            "stop": 85,
            "len": 85,
            "grp": 1,
            "spc": 0,
            "on": True,
            "bri": 255,
            "col": [[255, 0, 255], [0, 0, 0], [0, 0, 0]],
            "fx": 9,
            "sx": 128,
            "ix": 128,
            "pal": 1,
            "sel": True,
            "rev": False,
            "mi": False,
        }
    ],
}


wled_device_ip = "10.10.10.125"

api_endpoint = f"http://{wled_device_ip}/json/"

wled_headers = {"content-type": "application/json"}


def get_info():
    r = requests.get(api_endpoint)
    return r.json()


def set_state(data):
    r = requests.post(api_endpoint + "/state", data=json.dumps(data), headers=wled_headers)
    # print(r.status_code)
    return r


# print(get_info())
# set_state(wled_basic)
set_state(wled_rainbow)
