import pprint
from time import sleep

from humanfriendly import format_timespan
from nut2 import PyNUTClient as clientNut

HOST_ADDR = "ups.computeerror.com"
HOST_USER = "netwokz"
HOST_PASS = "emagdnim9"


"""
'battery.charge': '100',
'battery.runtime': '2254',
'battery.voltage': '54.80',
'input.voltage': '121.60',
'output.current': '3',
'output.voltage': '121.60',
'ups.load': '30.10',
'ups.model': 'Smart-UPS X 1500',
'ups.power': '378',
'ups.realpower': '361',
'ups.serial': 'AS1624236675',
'ups.status': 'OL',
'ups.temperature': '20.40',
'ups.test.date': '11/29/2023',
'ups.test.result': 'Ok'
"""


def parse_ups_stats(stats):
    ups_battery_charge = stats["battery.charge"]
    ups_battery_runtime = stats["battery.runtime"]
    ups_battery_voltage = stats["battery.voltage"]

    ups_input_voltage = stats["input.voltage"]

    ups_output_voltage = stats["output.voltage"]
    ups_output_current = stats["output.current"]

    ups_load = stats["ups.load"]
    ups_model = stats["ups.model"]
    ups_power = stats["ups.power"]
    ups_real_power = stats["ups.realpower"]
    ups_serial = stats["ups.serial"]
    ups_status = stats["ups.status"]
    ups_temp = stats["ups.temperature"]
    ups_last_test_date = stats["ups.test.date"]
    ups_last_test_result = stats["ups.test.result"]

    print(f"Battery is at {ups_battery_charge}%")
    print(f"Server will run for {ups_battery_runtime} mins")
    print(f"Batterys are at {ups_battery_voltage}v")

    print(f"Input Voltage is {ups_input_voltage}v")

    print(f"Output Voltage is {ups_output_voltage}v")
    print(f"Output Current is {ups_output_current}A")

    print(f"Load is {ups_load}%")
    print(f"Model is {ups_model}%")
    print(f"Power is {ups_power}%")
    print(f"Real Power is {ups_real_power}%")
    print(f"Serial is {ups_serial}")
    print(f"Status is {ups_status}")
    print(f"Temperature is {ups_temp}°")
    print(f"Last Test Date is {ups_last_test_date}")
    print(f"Last Test Result was {ups_last_test_result}")


def get_ups_stats():
    client = clientNut(host=HOST_ADDR, login=HOST_USER, password=HOST_PASS, debug=True)
    ups_all_stats = client.list_vars("rack-ups")
    sleep(2)
    parse_ups_stats(ups_all_stats)


get_ups_stats()
