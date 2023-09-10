from pylogix import PLC
from datetime import datetime
import asyncio
import json
import requests

sorters = {
    "AFE1" : "10.79.218.12",
    "AFE2" : "10.79.219.12",
    "SHP" : "10.79.216.201",
    "MRS" : "10.79.216.171"
}


async def multi_ping(sp, ip):
  with PLC(ip) as comm:
        # print(f"Checking {sp}")
        no_alarm = comm.Read("Alarm_Faults_None")
        if no_alarm.Value == True:
            # print("No alarms currently active")
            return
        for x, y in alarms_critical.items():
            temp = comm.Read(x)
            if temp.Value == True:
              # await send_webhook(f"{sp} is down with fault: {y} ")  
              print(f"{sp} is down with fault: {y} ")  
        # print("\n")


async def main():
  for sl2, ip in sorters.items():
    await multi_ping(sl2,ip)