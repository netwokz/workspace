#!/usr/bin/env python3

from nut2 import PyNUTClient as clientNut

HOST_ADDR = "10.10.10.152"
HOST_USER = "netwokz"
HOST_PASS = "emagdnim9"


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

    # print(f"Battery is at {ups_battery_charge}%")
    # print(f"Server will run for {ups_battery_runtime} mins")
    # print(f"Batterys are at {ups_battery_voltage}v")

    # print(f"Input Voltage is {ups_input_voltage}v")

    # print(f"Output Voltage is {ups_output_voltage}v")
    # print(f"Output Current is {ups_output_current}A")

    # print(f"Load is {ups_load}%")
    # print(f"Model is {ups_model}%")
    # print(f"Power is {ups_power}%")
    # print(f"Real Power is {ups_real_power}%")
    # print(f"Serial is {ups_serial}")
    # print(f"Status is {ups_status}")
    # print(f"Temperature is {ups_temp}°")
    # print(f"Last Test Date is {ups_last_test_date}")
    # print(f"Last Test Result was {ups_last_test_result}")


def get_ups_stats():
    client = clientNut(host=HOST_ADDR, login=HOST_USER, password=HOST_PASS, debug=True)
    ups_name = list(client.list_ups())[0]
    ups_all_stats = client.list_vars(ups_name)
    final_string = ""

    for key, value in ups_all_stats.items():
        # Different manufacturers use different values (floats vs strings) for specific fields
        # Matches device.serial, ups.serial, and ups.vendorid
        matches = [".serial", ".vendorid"]

        # First, check for any keys containing strings from above and set those values to strings
        if any(x in key for x in matches):
            value = f'"{value}"'
        else:
            try:
                # If the value is a float, ok
                float(value)
            except ValueError:
                # If the value is not a float (i.e., a string), then wrap it in quotes (this is needed for Influx's line protocol)
                value = f'"{value}"'

        # Create a single data point, then append that data point to the string
        data_point = f"{key}={value},"
        final_string += data_point

    # Format is "measurment tag field(s)", stripping off the final comma
    # print("ups," + "ups_name=" + ups_name, final.rstrip(","))
    return final_string


get_ups_stats()
