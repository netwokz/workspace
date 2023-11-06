from pylogix import PLC
import sqlite3
import os
from datetime import datetime
from contextlib import closing
import json
import requests
from time import sleep

tote_stacker_dict = {
    "Tote Stacker 1": "10.79.219.62",
    "Tote Stacker 2": "10.79.219.61",
    "Tote Stacker 3": "10.79.219.60",
    "Tote Stacker 4": "10.79.219.55"
}

tags = ["AnyMachineFault", "EstopActive", "TilitedStack_Detected",
        "TiltedStack", "ConveyorJam", "GripperFault"]

CURRENT_DIR = os.getcwd()
DB_NAME = "tote_stacker.db"
start = datetime.now()


def get_user_folder():
    if os.name == "nt":
        return f"{os.getenv('USERPROFILE')}\\"
    else:  # PORT: For *Nix systems
        return f"{os.getenv('HOME')}/"


def does_table_exist():
    with closing(sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tote_stacker_table' ''')
            # if the count is 1, then table exists
            if cursor.fetchone()[0] == 1:
                # Table exists
                return True
            else:
                # Table does not exist.
                cursor.execute(
                    "CREATE TABLE tote_stacker_table (name TEXT, entry TEXT, time TEXT)")
                return False


does_table_exist()


def send_webhook(my_data):
    web_hook_link = 'https://hooks.slack.com/workflows/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'
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"wo_id": my_data})
    response = requests.post(web_hook_link, headers=headers, data=data)
    print(response)


def add_entry(name):
    with closing(sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))) as conn:
        with closing(conn.cursor()) as cursor:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute(
                "INSERT INTO tote_stacker_table (name,entry,time) VALUES (?,?,?)", (name, "DOWN", dt_string))
            conn.commit()


def has_entry(name):
    with closing(sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))) as conn:
        with closing(conn.cursor()) as cursor:
            rows = cursor.execute(
                "SELECT name FROM tote_stacker_table WHERE name = ?", (name,)).fetchall()
            for row in rows:
                if row is not None:
                    return True
                else:
                    return False


def update_entry(name):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with closing(sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "UPDATE tote_stacker_table SET time = ? WHERE name = ?", (dt_string, name))
            conn.commit()


def delete_entry(name):
    with closing(sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM tote_stacker_table WHERE name = ?", (name,))
            conn.commit()


def getDuration(then, now=datetime.now(), interval="default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

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


def ping_tote_stacker():
    for id, ip in tote_stacker_dict.items():
        with PLC(ip) as comm:
            # print(id)
            # for tag in tags:
            #     value = comm.Read(tag)
            value = comm.Read("AnyMachineFault")
            if value.Value == True:
                # send_webhook(f"{id} is down")
                if has_entry(id):
                    update_entry(id)
                else:
                    add_entry(id)
            else:
                if has_entry(id):
                    delete_entry(id)

# for item in tote_stacker_dict.keys():
#     has_entry(item)


count = 0
while count < 3:
    ping_tote_stacker()
    count += 1
    sleep(5)

end = datetime.now()

print(getDuration(start, end))
print(f"Ran {count} times")
