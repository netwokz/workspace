from plyer import notification
from pylogix import PLC


def send_notification(title, msg, timeout=10):
    notification.notify(
        title=title,
        message=msg,
        app_icon=r"C:\Users\deanejst\Documents\CODE\workspace\PLC\smart-pac.ico",
        timeout=timeout,
    )


def get_stats(ip):
    with PLC(ip) as comm:
        stat = comm.Read("IS21_ES_PB1")
        if stat.Value is None:
            stat.Value = "Oops!"
        send_notification("SmartPac", f"ESTOP condition is {stat.Value}")
        print(stat.Value)


get_stats("10.79.216.223")
