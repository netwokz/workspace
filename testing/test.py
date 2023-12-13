import json
import os
import re
from datetime import date

import requests
from fleet_health_checker import FleetHealthCheck as fhc

json_response = None
folder_path = os.path.expanduser(r"~\Documents\CODE\workspace\testing")
# network_folder_path = r"\\ant\dept-na\GYR1\Support\NACF-AE\Master_IP_Addresses"
re_pattern = "(\d+-\d+-\d+)"
# re_pattern_op = "(\d{8})"


def pull_health_report():
    today = date.today()
    azptl = fhc("GYR1")
    health_report = json.loads(azptl.get_health_report())
    global json_response
    json_response = json.dumps(health_report, indent=2)
    with open(f"health_report_{today}.json", "w") as outfile:
        outfile.write(json_response)


def load_health_report():
    with open("health_report.json", "r") as openfile:
        global json_response
        json_response = json.load(openfile)


def parse_file_name(filename):
    match = re.search(re_pattern, filename)
    return match.group(1)


def get_file_names(search_path):
    result = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith(".json"):
                # if file.endswith(".xlsx"):
                result.append(str(file))
    return result


def compare_files(file):
    new_datetime = date.fromisoformat(parse_file_name(file))
    delta = date.today() - new_datetime
    print(delta.days)
    if delta.days > 7:
        # pull_health_report()
        print("Health report is out of date!")


health_files = get_file_names(folder_path)
compare_files(health_files[0])
