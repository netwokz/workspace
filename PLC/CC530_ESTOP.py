import re
from time import sleep

from plyer import notification
from pylogix import PLC

found_estops = []
regex_pattern = "IS[0-9]+"


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


def parse_name(name):
    result = re.findall(regex_pattern, name)
    return result[0]


def save_estop_state(state):
    with open("myfile.txt", "w") as file1:
        file1.writelines(state)


def get_stats(ip):
    with PLC(ip) as comm:
        # while True:
        nc_ret = comm.Read(is_estops)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in nc_ret:
            if tag.Value == False:
                print(f"E-Stop condition at {parse_name(tag.TagName)}")
                save_estop_state(tag.TagName)
        gate_ret = comm.Read(is_gates)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in gate_ret:
            if tag.Value == True:
                print(f"E-Stop condition at {parse_name(tag.TagName)}")
                save_estop_state(tag.TagName)
        sleep(0.5)


get_stats("10.79.216.223")
