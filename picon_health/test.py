import json
import os
import re
from datetime import date

from fleet_health_checker import FleetHealthCheck as fhc

json_response = None
folder_path = os.path.expanduser(r"~\Documents\CODE\workspace\picon_health")
# network_folder_path = r"\\ant\dept-na\GYR1\Support\NACF-AE\Master_IP_Addresses"
re_pattern = r"(\d+-\d+-\d+)"
# re_pattern_op = "(\d{8})"


def pull_health_report():
    today = date.today()
    azptl = fhc("GYR1")
    health_report = json.loads(azptl.get_health_report())
    response = json.dumps(health_report, indent=2)
    if response is not None:
        with open(f"health_report_{today}.json", "w") as outfile:
            outfile.write(response)


def load_health_report(filename):
    with open(filename, "r") as openfile:
        global json_response
        json_response = json.load(openfile)


def parse_file_name(filename):
    match = re.search(re_pattern, filename)
    return match.group(1)


def parse_wall_name(wall_name):
    match = re.search(r"\d\d.*", wall_name)
    return match.group(0)


def get_latest_filename():
    result = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                result.append(str(file))
        break
    result.reverse()
    if len(result) > 1:
        for filename in result[1:]:
            os.remove(filename)
    if len(result) == 0:
        result = None
    return result[0]


def compare_files(file):
    new_datetime = date.fromisoformat(parse_file_name(file))
    delta = date.today() - new_datetime
    if delta.days > 7:
        print("Health report is out of date, pulling new data")
        pull_health_report()


def check_health_report():
    health_file = get_latest_filename()
    if health_file == None:
        pull_health_report()
    else:
        compare_files(health_file)

    load_health_report(get_latest_filename())


def parse_health_report():
    for wall in json_response["controllers"]:
        wall_id = parse_wall_name(wall["StationID"])
        wall_health = wall["Health"]
        if wall_health < 100 and wall_health > 0:
            print(f"{wall_id}: {wall_health}")
        if wall_health == -1:
            print(f"{wall_id} PiCon is Offline")


check_health_report()
parse_health_report()
