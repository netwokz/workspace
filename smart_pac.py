from pylogix import PLC
from datetime import datetime
import json
import requests
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

cur_sp_errors = []

sp_dict = {
    "SP 5-1": "10.18.8.137",
    "SP 5-2": "10.18.8.140",
    "SP 5-3": "10.18.8.143",
    "SP 5-4": "10.18.8.146",
    "SP 5-5": "10.18.8.149",
    "SP 6-6": "10.18.8.152",
    "SP 6-7": "10.18.8.155",
    "SP 6-8": "10.18.8.158",
    "SP 6-9": "10.18.8.161",
    "SP 6-10": "10.18.8.164",
    "SP 7-11": "10.18.8.167",
    "SP 7-12": "10.18.8.170",
    "SP 7-13": "10.18.8.173",
    "SP 7-14": "10.18.8.176",
    "SP 7-15": "10.18.8.179",
    "SP TEST": "10.18.8.180"
}

non_critical_alarms = {
    "Alarm_Fault[0].5": "Nip Not Closed",
    "Alarm_Fault[0].6": "Nip Interference",
    "Alarm_Fault[0].10": "Bag Material Roll Out of Position",
    "Alarm_Fault[0].20": "Printer Faulted",
    "Alarm_Fault[0].21": "Applicator Tamp Failed To Return",
    "Alarm_Fault[0].22": "Labeler Cycle Too Long",
    "Alarm_Fault[0].26": "Verify Camera Offline",
    "Alarm_Fault[0].27": "Verify Camera Cycle too Long",
    "Alarm_Fault[0].28": "Fault Sealer Bar Temperature Too Low",
    
}

critical_alarms = {
    "Alarm_Fault[0].0": "Area Not Clear",
    "Alarm_Fault[0].1": "Jaw Not Clear",
    "Alarm_Fault[0].2": "Feed Fault",
    "Alarm_Fault[0].3": "Gripper Servo Current High",
    "Alarm_Fault[0].4": "Nip Fault",
    "Alarm_Fault[0].7": "Product Sensor Fault",
    "Alarm_Fault[0].8": "Gripper Fault Movement Overtime",
    "Alarm_Fault[0].9": "Cycle Fault",
    "Alarm_Fault[0].12": "Air Pressure Low",
    "Alarm_Fault[0].14": "Grip Obstructing Seal Cycle",
    "Alarm_Fault[0].15": "Takeaway Conveyor Motor Fault",
    "Alarm_Fault[0].16": "Kick Out Conveyor Motor Fault",
    "Alarm_Fault[0].17": "Takeaway Conveyor PE Jam Fault",
    "Alarm_Fault[0].18": "Kickout Conveyor PE Jam Fault",
    "Alarm_Fault[0].19": "Tote Barcode Reader Offline",
    "Alarm_Fault[0].23": "Labeler Printing Failed Fault",
    "Alarm_Fault[0].24": "Labeler Tamp Head Vacuum Fault",
    "Alarm_Fault[0].25": "Applicator Failed to Tamp Fault",
    "Alarm_Fault[0].29": "Divert Position Timeout Fault",
    "Alarm_Fault[0].30": "Package Lost After Sealing Cycle",
    "Alarm_Fault[1].2": "Printer Not In FWD Position",
    "Alarm_Fault[1].3": "Grip Fault Gripper Home Sensor Not Found",
    "Alarm_Fault[1].4": "Gripper Servo  Axis Fault",
    "Alarm_Fault[1].5": "Gripper Servo Down Position Limit Incorrect",
    "Alarm_Fault[1].6": "Fault Gripper Overtravel Upper",
    "Alarm_Fault[1].7": "Fault Gripper Overtravel Lower",
    "Alarm_Fault[1].8": "Nip Servo Axis Fault",
    "Alarm_Fault[1].10": "Kinetix Servo Ethernet Communication Error",
    "Alarm_Fault[1].11": "PowerFlex Ethernet Communication Error",
    "Alarm_Fault[1].12": "Fault Jaw Open",
    "Alarm_Fault[1].13": "Fault Jaw Close",
    "Alarm_Fault[1].14": "Fault Jaw Safety Sensor (Operator Side)",
    "Alarm_Fault[1].15": "Fault Jaw Safety Sensor (Roll Side)",
    "Alarm_Fault[1].16": "Gripper Adv/Ret Cycle Fault",
    "Alarm_Fault[1].17": "Gripper Open/Close Cycle Fault",
    "Alarm_Fault[1].20": "Jaw Safeties Obstrucing Seal Jaw",
    "Alarm_Fault[1].21": "Jaw Not Clear Light Curtain blocked",
    "Alarm_Fault[1].22": "Jaw Not Clear Item sensor blocked",
    "Alarm_Fault[1].25": "E-Stop PB Operator Side HMI Cabinet",
    "Alarm_Fault[1].26": "E-Stop PB Back Side Film Roll Area",
    "Alarm_Fault[1].27": "E-Stop PB Back Side Exit Conveyor",
    "Alarm_Fault[1].28": "E-Stop Switch Operator Side Jaw Access Sliding Door",
    "Alarm_Fault[1].29": "E-Stop PB Operator Side Exit Conveyor",
    "Alarm_Fault[1].30": "Estop Relay Fault"
}


class SmartPac(Base):
    __tablename__ = 'smartpac'

    sp_name = Column('Name', String, primary_key=True)
    sp_alarm = Column('Alarm', String)
    sp_timestamp = Column('Timestamp', String)

    def __init__(self, sp_name, sp_alarm, sp_timestamp):
        self.sp_name = sp_name
        self.sp_alarm = sp_alarm
        self.sp_timestamp = sp_timestamp

    def get_name(self):
        return self.sp_name

    def get_df_data(self):
        sp_dict = {
            # "ID": self.sp_id,
            "Name": self.sp_name,
            "Alarm": self.sp_alarm,
            "Timestamp": self.sp_timestamp,
        }
        return sp_dict

    def __repr__(self):
        return f"Name: {self.sp_name}, Alarm: {self.sp_alarm}, Timestamp: {self.sp_timestamp}"

    def __hash__(self):
        return self.sp_id.__hash__

    def __eq__(self, other):
        # print("__eq__ called")
        return str(self.sp_name) == str(other.sp_name) and str(self.sp_alarm) == str(other.sp_alarm)


engine = create_engine(
    "sqlite:///C:/Users/deanejst/Documents/WEBHOOK/sp/mydb.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def compare_db_entries():
    db_sp_errors = get_all_entries()
    # cur_sp_errors = get_sp_data()

    if len(db_sp_errors) != 0 and len(cur_sp_errors) != 0:
        for smartpac in db_sp_errors:
            if smartpac not in cur_sp_errors:
                delete_entry(smartpac)
                print(f"SP {smartpac.getName()} deleted successfully")
            else:
                print(f"SP {smartpac.getName()} kept")

    # for smartpac in cur_sp_errors:
    #     if smartpac not in db_sp_errors:
    #         add_entry(smartpac)
    #     else:
    #         print(f"SP {smartpac.getName()} already exists")


def delete_entry(sp_entry: SmartPac):
    session.delete(sp_entry)
    session.commit()


def add_entry(sp_entry: SmartPac):
    db_sp_errors = get_all_entries()
    if len(db_sp_errors) != 0:
        if sp_entry not in db_sp_errors:
            print(f"SP {sp_entry.getName()} added to DB")
            session.add(sp_entry)
            session.commit()
        else:
            print(f"SP {sp_entry.getName()} already exists")


def get_all_entries() -> list[SmartPac]:
    results = session.query(SmartPac).all()
    return results


def get_df_values() -> pd.DataFrame:
    work_orders = get_all_entries()
    dict_list = []
    for wo in work_orders:
        # print(wo)
        dict_list.append(wo.get_df_data())
    wo_df = pd.DataFrame.from_dict(dict_list)
    return wo_df


def getDuration(then, now=datetime.now(), interval="default"):
    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        # Seconds in a day = 86400
        return divmod(seconds if seconds != None else duration_in_s, 86400)

    def hours(seconds=None):
        # Seconds in an hour = 3600
        return divmod(seconds if seconds != None else duration_in_s, 3600)

    def minutes(seconds=None):
        # Seconds in a minute = 60
        return divmod(seconds if seconds != None else duration_in_s, 60)

    def seconds(seconds=None):
        if seconds != None:
            return divmod(seconds, 1)
        return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
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
        no_alarm = comm.Read("CONST_ESP_USE_THIS.SUCCESS").Value
        if no_alarm == "SUCCESS":
            print(f"Connected to {sp} successfully")
        else:
            print(f"Could not connect to {sp}")

dum_alarms = ["Alarm_Faults_None","Operational_Mode_Manual_Active"]# "Operational_Mode_Auto_Active"

def get_sp_data():
    for sp, ip in sp_dict.items():
        with PLC(ip, timeout=2) as comm:
            test_connect = comm.Read("CONST_ESP_USE_THIS.SUCCESS").Value
            if test_connect == "SUCCESS":
                # Can successfully ping SmartPac
                values = comm.Read(dum_alarms)
                for ret in values:
                    if ret.Value == True:
                        print(f"{sp} has no issues. {ret.TagName}:{ret.Value}")
                        break
                else:
                    print(f"{sp} has issues.")
                    for x, y in critical_alarms.items():
                        temp = comm.Read(x)
                        if temp.Value == True:
                            smartpac = SmartPac(sp, y, str(datetime.now().astimezone().timestamp()))
                            # add_entry(smartpac)
                            cur_sp_errors.append(smartpac)
                            print(f"{sp}: {y} is {temp.Value}")


def send_webhook(my_data):
    # URL = "https://hooks.slack.com/workflows/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" # CBM Channel
    URL = "https://hooks.slack.com/workflows/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"  # My Message
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    print(response)

get_sp_data()
# compare_db_entries()
# print(get_all_entries())

# for sp, ip in sp_dict.items():
#     ping_sp(sp, ip)