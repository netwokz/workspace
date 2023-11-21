from time import sleep

from plyer import notification
from pylogix import PLC

found_estops = []


def send_notification(title, msg, timeout=5):
    notification.notify(
        title=title,
        message=msg,
        app_icon=r"C:\Users\deanejst\Documents\CODE\workspace\PLC\smart-pac.ico",
        timeout=timeout,
    )


nc_estops = [
    "IS11_ES_PB1",
    "IS12_ES_PB1",
    "IS13_ES_PB1",
    "IS14_ES_PB1",
    "IS15_ES_PB1",
    "IS16_ES_PB1",
    "IS17_ES_PB1",
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
    "IS17_ES_PB2",
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


def get_stats(ip):
    with PLC(ip) as comm:
        # while True:
        nc_ret = comm.Read(nc_estops)
        # send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        for tag in nc_ret:
            if tag.Value == False:
                print(f"{tag.TagName} is {tag.Value}")

        sleep(0.5)


get_stats("10.79.216.223")
