import json
import re
from time import sleep, time

import requests
from plyer import notification
from pylogix import PLC

MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data

found_estops = {}
regex_pattern = "IS[0-9]+"
regex_pattern_gate = "MAINT[0-9]+"


def send_notification(title, msg, timeout=5):
    notification.notify(
        title=title,
        message=msg,
        app_icon=r"C:\Users\deanejst\Documents\CODE\workspace\PLC\smart-pac.ico",
        timeout=timeout,
    )


is_estops = [
    "IS11_ES_PB1",
    "IS12_ES_PB1",
    "IS13_ES_PB1",
    "IS14_ES_PB1",
    "IS15_ES_PB1",
    "IS16_ES_PB1",
    # "IS17_ES_PB1",
    "IS18_ES_PB1",
    "IS21_ES_PB1",
    "IS22_ES_PB1",
    "IS23_ES_PB1",
    "IS24_ES_PB1",
    "IS25_ES_PB1",
    "IS26_ES_PB1",
    "IS11_ES_PB2",
    "IS12_ES_PB2",
    "IS13_ES_PB2",
    "IS14_ES_PB2",
    "IS15_ES_PB2",
    "IS16_ES_PB2",
    # "IS17_ES_PB2",
    "IS18_ES_PB2",
    "IS21_ES_PB2",
    "IS22_ES_PB2",
    "IS23_ES_PB2",
    "IS24_ES_PB2",
    "IS25_ES_PB2",
    "IS26_ES_PB2",
    "I_GATE1_OK",
    "I_GATE2_OK",
]

is_gates = [
    "IS11_GATE_OPEN",
    "IS12_GATE_OPEN",
    "IS13_GATE_OPEN",
    "IS14_GATE_OPEN",
    "IS15_GATE_OPEN",
    "IS16_GATE_OPEN",
    "IS17_GATE_OPEN",
    "IS18_GATE_OPEN",
    "IS21_GATE_OPEN",
    "IS22_GATE_OPEN",
    "IS23_GATE_OPEN",
    "IS24_GATE_OPEN",
    "IS25_GATE_OPEN",
    "IS26_GATE_OPEN",
    "IS27_GATE_OPEN",
    "IS28_GATE_OPEN",
]

is_maint_gates = [
    "MAINT1_GATE_OPEN",
    "MAINT2_GATE_OPEN",
]


def send_fail_notification():
    URL = MY_TEST_URL
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps({"data": "E-Stop Webhook failed"})
    response = requests.post(URL, headers=headers, data=data)
    # print(response.status_code)


def send_webhook(url, my_data):
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps({"data": my_data})
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.status_code != 200:
        send_fail_notification()


def parse_name(name):
    result = re.findall(regex_pattern, name)
    return result[0]


def parse_maint_name(name):
    result = re.findall(regex_pattern_gate, name)
    return result[0]


def save_estop_state(state):
    with open("myfile.txt", "w") as file1:
        file1.writelines(state)


def check_estops(ip):
    no_faults = True
    with PLC(ip) as comm:
        # while True:
        nc_ret = comm.Read(is_estops)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in nc_ret:
            if tag.Value == False:
                no_faults = False
                if tag.TagName in found_estops:
                    curr_milliseconds = int(time() * 1000)
                    if curr_milliseconds - found_estops[tag.TagName] > 300000:
                        send_notification("E-Stop!", f"E-Stop condition at {parse_name(tag.TagName)}")
                        break
                milliseconds = int(time() * 1000)
                found_estops[tag.TagName] = milliseconds
                print(f"E-Stop condition at {parse_name(tag.TagName)}")

        gate_ret = comm.Read(is_gates)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in gate_ret:
            if tag.Value == True:
                no_faults = False
                if tag.TagName in found_estops:
                    curr_milliseconds = int(time() * 1000)
                    if curr_milliseconds - found_estops[tag.TagName] > 300000:
                        send_notification("E-Stop!", f"E-Stop condition at {parse_name(tag.TagName)}")
                        break
                print(f"E-Stop condition at {parse_name(tag.TagName)}")
                milliseconds = int(time() * 1000)
                found_estops[tag.TagName] = milliseconds

        maint_gate_ret = comm.Read(is_maint_gates)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in maint_gate_ret:
            no_faults = False
            if tag.Value == True:
                if tag.TagName in found_estops:
                    curr_milliseconds = int(time() * 1000)
                    if curr_milliseconds - found_estops[tag.TagName] > 300000:
                        send_notification("E-Stop!", f"E-Stop condition at {parse_maint_name(tag.TagName)}")
                        break
                milliseconds = int(time() * 1000)
                found_estops[tag.TagName] = milliseconds
                print(f"E-Stop condition at {parse_maint_name(tag.TagName)}")
        if no_faults:
            found_estops.clear()


check_estops("10.79.216.223")
