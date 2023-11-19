import json
import subprocess
import time
from datetime import datetime


def check_wifi_status():
    current_properties = {"State": "false", "Signal": "-1", "SSID": "asin", "Channel": "000"}
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
        output = result.stdout

        # Get the current connection status
        start_conn = output.index("State") + len("State") + 1
        end_conn = output.index("\n", start_conn)
        current_properties["State"] = output[start_conn:end_conn].strip(" :")

        # Get the current connection signal strength
        start_signal = output.index("Signal") + len("Signal") + 1
        end_signal = output.index("\n", start_signal)
        current_properties["Signal"] = output[start_signal:end_signal].strip(" :")

        # Get the current connection status
        start_ssid = output.index("SSID") + len("SSID") + 1
        end_ssid = output.index("\n", start_ssid)
        current_properties["SSID"] = output[start_ssid:end_ssid].strip(" :")

        # Get the current connection status
        start_chan = output.index("Channel") + len("Channel") + 1
        end_chan = output.index("\n", start_chan)
        current_properties["Channel"] = output[start_chan:end_chan].strip(" :")

        return current_properties

    except Exception as e:
        return f"Error occurred: {e}"


def log_entry(entry):
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("log.txt", "a") as file:
        log_string = f"{now_string}: {entry['State']} to {entry['SSID']}, at {entry['Signal']} on channel {entry['Channel']}"
        file.write("\n" + log_string)


if __name__ == "__main__":
    while True:
        wifi_status = check_wifi_status()
        # if wifi_status["State"] != "Connected":
        log_entry(wifi_status)
        time.sleep(1)  # Adjust the delay as needed (in seconds)
