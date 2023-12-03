import pprint

from humanfriendly import format_timespan
from nut2 import PyNUTClient as clientNut
from PyNUT import PyNUTClient

client = clientNut()
client.help()
client.list_ups()
client.list_vars("rack-ups")

HOST_ADDR = "10.10.10.152"
HOST_USER = "netwokz"
HOST_PASS = "emagdnim9"

"""
    "battery.charge": "100",
    "battery.charge.low": "10",
    "battery.charge.warning": "50",
    "battery.runtime": "2254",
    "battery.runtime.low": "150",
    "battery.type": "PbAc",
    "battery.voltage": "54.8",
    "battery.voltage.nominal": "48.0",
    "device.mfr": "American Power Conversion ",
    "device.model": "Smart-UPS X 1500",
    "device.serial": "AS1624236675  ",
    "device.type": "ups",
    "driver.name": "usbhid-ups",
    "driver.parameter.pollfreq": "30",
    "driver.parameter.pollinterval": "1",
    "driver.parameter.port": "auto",
    "driver.parameter.productid": "0003",
    "driver.parameter.serial": "AS1624236675",
    "driver.parameter.synchronous": "auto",
    "driver.parameter.vendorid": "051D",
    "driver.version": "2.8.0",
    "driver.version.data": "APC HID 0.98",
    "driver.version.internal": "0.47",
    "driver.version.usb": "libusb-1.0.26 (API: 0x1000109)",
    "ups.beeper.status": "enabled",
    "ups.delay.shutdown": "20",
    "ups.firmware": "UPS 09.1 / ID=20",
    "ups.mfr": "American Power Conversion ",
    "ups.mfr.date": "2016/06/20",
    "ups.model": "Smart-UPS X 1500",
    "ups.productid": "0003",
    "ups.serial": "AS1624236675  ",
    "ups.status": "OL",
    "ups.timer.reboot": "-1",
    "ups.timer.shutdown": "-1",
    "ups.vendorid": "051d",
"""


def get_ups_stats():
    ups = PyNUTClient(host=HOST_ADDR, login=HOST_USER, password=HOST_PASS)
    ups_stats = ups.GetUPSVars(ups="rack-ups")
    return ups_stats


# pprint.pprint(get_ups_stats())
