from pylogix import PLC
from datetime import datetime
import asyncio
import json
import requests

start = datetime.now()

sp_dict = {
    "SmartPac 5-1" : "10.18.8.137",
    "SmartPac 5-2" : "10.18.8.140",
    "SmartPac 5-3" : "10.18.8.143",
    "SmartPac 5-4" : "10.18.8.146",
    "SmartPac 5-5" : "10.18.8.149",
    "SmartPac 6-6" : "10.18.8.152",
    "SmartPac 6-7" : "10.18.8.155",
    "SmartPac 6-8" : "10.18.8.158",
    "SmartPac 6-9" : "10.18.8.161",
    "SmartPac 6-10" : "10.18.8.164",
    "SmartPac 7-11" : "10.18.8.167",
    "SmartPac 7-12" : "10.18.8.170",
    "SmartPac 7-13" : "10.18.8.173",
    "SmartPac 7-14" : "10.18.8.176",
    "SmartPac 7-15" : "10.18.8.179"
}

alarms_non_critical = {
        "Alarm_Fault[0].0" : "Area Not Clear",
        "Alarm_Fault[0].1" : "Jaw Not Clear",
        "Alarm_Fault[0].6" : "Nip Interference",
        "Alarm_Fault[0].7" : "Product Sensor Fault",
        "Alarm_Fault[0].10" : "Bag Material Roll Out of Position",
        "Alarm_Fault[0].20" : "Printer Faulted",
        "Alarm_Fault[0].22" : "Labeler Cycle Too Long",
        "Alarm_Fault[0].23" : "Labeler Printing Failed Fault",
        "Alarm_Fault[0].24" : "Labeler Tamp Head Vacuum Fault",
        "Alarm_Fault[0].25" : "Applicator Failed to Tamp Fault",
        "Alarm_Fault[1].20" : "Jaw Safeties Obstrucing Seal Jaw",
        "Alarm_Fault[1].21" : "Jaw Not Clear Light Curtain blocked",
        "Alarm_Fault[1].22" : "Jaw Not Clear Item sensor blocked",
        "Alarm_Fault[0].27" : "Verify Camera Cycle too Long"
}

alarms_critical = {
        
        "Alarm_Fault[0].2" : "Feed Fault",
        "Alarm_Fault[0].3" : "Gripper Servo Current High",
        "Alarm_Fault[0].4" : "Nip Fault",
        "Alarm_Fault[0].5" : "Nip Not Closed",
        "Alarm_Fault[0].8" : "Gripper Fault Movement Overtime",
        "Alarm_Fault[0].9" : "Cycle Fault",
        "Alarm_Fault[0].12" : "Air Pressure Low",
        "Alarm_Fault[0].14" : "Grip Obstructing Seal Cycle",
        "Alarm_Fault[0].15" : "Takeaway Conveyor Motor Fault",
        "Alarm_Fault[0].16" : "Kick Out Conveyor Motor Fault",
        "Alarm_Fault[0].17" : "Takeaway Conveyor PE Jam Fault",
        "Alarm_Fault[0].18" : "Kickout Conveyor PE Jam Fault",
        "Alarm_Fault[0].19" : "Tote Barcode Reader Offline",
        "Alarm_Fault[0].21" : "Applicator Tamp Failed To Return",
        "Alarm_Fault[0].26" : "Verify Camera Offline",
        "Alarm_Fault[0].28" : "Fault Sealer Bar Temperature Too Low",
        "Alarm_Fault[0].29" : "Divert Position Timeout Fault",
        "Alarm_Fault[0].30" : "Package Lost After Sealing Cycle",
        "Alarm_Fault[1].2" : "Printer Not In FWD Position",
        "Alarm_Fault[1].3" : "Grip Fault Gripper Home Sensor Not Found",
        "Alarm_Fault[1].4" : "Gripper Servo Axis Fault",
        "Alarm_Fault[1].5" : "Gripper Servo Down Position Limit Incorrect",
        "Alarm_Fault[1].6" : "Fault Gripper Overtravel Upper",
        "Alarm_Fault[1].7" : "Fault Gripper Overtravel Lower",
        "Alarm_Fault[1].8" : "Nip Servo Axis Fault",
        "Alarm_Fault[1].10" : "Kinetix Servo Ethernet Communication Error",
        "Alarm_Fault[1].11" : "PowerFlex Ethernet Communication Error",
        "Alarm_Fault[1].12" : "Fault Jaw Open",
        "Alarm_Fault[1].13" : "Fault Jaw Close",
        "Alarm_Fault[1].14" : "Fault Jaw Safety Sensor (Operator Side)",
        "Alarm_Fault[1].15" : "Fault Jaw Safety Sensor (Roll Side)",
        "Alarm_Fault[1].16" : "Gripper Adv/Ret Cycle Fault",
        "Alarm_Fault[1].17" : "Gripper Open/Close Cycle Fault",
        "Alarm_Fault[1].25" : "E-Stop PB Operator Side HMI Cabinet",
        "Alarm_Fault[1].26" : "E-Stop PB Back Side Film Roll Area",
        "Alarm_Fault[1].27" : "E-Stop PB Back Side Exit Conveyor",
        "Alarm_Fault[1].28" : "E-Stop Switch Operator Side Jaw Access Sliding Door",
        "Alarm_Fault[1].29" : "E-Stop PB Operator Side Exit Conveyor",
        "Alarm_Fault[1].30" : "Estop Relay Fault"
}

def getDuration(then, now = datetime.now(), interval = "default"):
    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]

def ping_sp(sp, ip):
    with PLC(ip) as comm:
        no_alarm = comm.Read("Alarm_Faults_None")
        if no_alarm.Value == True:
            # print("No alarms currently active")
            return
        for x, y in alarms_critical.items():
            temp = comm.Read(x)
            if temp.Value == True:
                print(f"{sp}: {y} is {temp.Value}")  
        print("\n")

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

async def send_webhook(my_data):
    # URL = "https://hooks.slack.com/workflows/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" # CBM Channel
    URL = "https://hooks.slack.com/workflows/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" # My Message
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    print(response)

async def main():
  for sp, ip in sp_dict.items():
    await multi_ping(sp,ip)

# count = 0
# while count < 38:
#     for sp, ip in sp_dict.items():
#         ping_sp(sp, ip)
#     count += 1
#     sleep(5)

# end = datetime.now()

# print(getDuration(start, end))
# print(f"Ran {count} times")

while True:
  asyncio.run(main())