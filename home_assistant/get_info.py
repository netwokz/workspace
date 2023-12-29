import json as js
import os

from requests import get, post

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiYjY0OWNkZjVlYjU0NjY2YmZjNThkYzZmMWIxYTdkYSIsImlhdCI6MTcwMzcxMzc3NSwiZXhwIjoyMDE5MDczNzc1fQ.tN4vrUUxmphPlcfouY2AdKIL_mkgW7GbVBue253hc3s",
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


def set_wled_status(state):
    if state == "on":
        URL = "http://homeassistant.computeerror.com:8123/api/services/light/turn_on"
    else:
        URL = "http://10.10.10.7:8123/api/services/light/turn_off"
    data = {"entity_id": "switch.kitchen_light", "rgb_color": [255, 0, 0], "brightness": 76}
    response = post(URL, headers=headers, json=data)
    print(response.status_code)
    # print(js.dumps(response.json(), indent=2))


# set_wled_status("off")

# set_wled_status("on")


def turn_kitchen_light_on():
    URL = "http://10.10.10.7:8123/api/services/switch/turn_on"
    data = {"entity_id": "switch.kitchen_light"}
    response = post(URL, headers=headers, json=data)
    print(response.status_code)


def turn_kitchen_light_off():
    URL = "http://10.10.10.7:8123/api/services/switch/turn_off"
    data = {"entity_id": "switch.kitchen_light"}
    response = post(URL, headers=headers, json=data)
    print(response.status_code)


def get_all_services():
    all_services = []
    URL = "http://10.10.10.7:8123/api/services"
    response = get(URL, headers=headers)
    res_json = response.json()
    # print(res_json[0]["domain"])
    for service in res_json:
        # print(service["domain"])
        if service["domain"] == "switch":
            print(js.dumps(service, indent=2))
        all_services.append(service["domain"])

    # all_services = sorted(all_services)
    # for service in all_services:
    # print(service)
    # pass


# get_all_services()
# turn_kitchen_light_on()
# turn_kitchen_light_off()
