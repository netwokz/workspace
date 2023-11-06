import asyncio
import json
from datetime import datetime

import requests
from pylogix import PLC

sorters = {"AFE1": "10.79.218.12", "AFE2": "10.79.219.12", "SHP": "10.79.216.201", "MRS": "10.79.216.171"}


def multi_ping(sp, ip):
    with PLC(ip) as comm:
        print(f"Checking {sp}")
        speed = comm.Read("SORT_SPD.SORT_SPD_REQ")
        # if speed.Value is not None:
        print(f"Speed is {speed} ")
        # print("\n")


def main():
    for sl2, ip in sorters.items():
        multi_ping(sl2, ip)


main()
