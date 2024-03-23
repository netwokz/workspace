import csv
import datetime
import json
import os
from pathlib import Path
from textwrap import indent
from urllib.request import urlopen

date = datetime.datetime.now()
date = date - datetime.timedelta(days=1)
new_format = "%m/%d/%Y"
current_date = date.strftime(new_format)
working_dir = r"C:\Users\deanejst\Documents\CODE\workspace\python\water_util\csv_data"
# working_dir = r"C:\Users\netwokz\Documents\CODE\workspace\python\water_util\csv_data"
current_date = "01/31/2024"
daily_data = ""


def get_data_json(daily_date):
    URL = f"https://beaz-p-ia-wb.itron-hosting.com/AnalyticsCustomerPortal_BEAZ_PROD/PortalServices/api/UsageData/Interval/?servicePointId=26329&accountId=988503-522366&skipHours=0&takeHours=24&endDate={daily_date}"
    # store the response of URL
    response = urlopen(URL)
    data_json = json.loads(response.read())
    return data_json


def get_last_data_date():
    most_recent_file = None
    most_recent_time = 0
    for root, dirs, files in os.walk(working_dir):
        for filename in files:
            # Do Something With File
            # if root.endswith(str(date.month)):
            # print(os.path.join(root, filename))
            # print(root)
            # print(filename)
            mFile = Path(os.path.join(root, filename))
            # get the modification time of the file using entry.stat().st_mtime_ns
            mod_time = mFile.stat().st_mtime_ns
            if mod_time > most_recent_time:
                # update the most recent file and its modification time
                most_recent_file = mFile.name
                most_recent_time = mod_time
        # for dirname in dirs:
        #     pass
        #     # Do Something With Dir
        #     if root.endswith(str(date.year)):
        #         if dirname.endswith(str(date.month)):
        #             print(root)
        #             print(os.path.join(root, dirname))

    # iterate over the files in the directory using os.scandir
    # for entry in os.scandir(working_dir):
    #     if entry.is_file():
    #         # get the modification time of the file using entry.stat().st_mtime_ns
    #         mod_time = entry.stat().st_mtime_ns
    #         if mod_time > most_recent_time:
    #             # update the most recent file and its modification time
    #             most_recent_file = entry.name
    #             most_recent_time = mod_time
    print(most_recent_file)


get_last_data_date()


def convert(datetime_str):
    # Example with the standard date and time format
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(datetime_str, date_format)
    # new_format = "%b %d, %Y"
    new_format = "%H:%M"
    new_date = date_obj.strftime(new_format)
    return new_date


def parse_daily_data(date):
    daily_data = get_data_json(date)
    daily_data_list = []
    for item in daily_data:
        if item["Usage"] is not None:
            usage = int((float(item["Usage"]) * 1000))
            if usage > 0:
                date = convert(item["Date"])
                daily_data_list.append([date, usage])

    return daily_data_list


def get_month_day():
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(daily_data[-1]["Date"], date_format)
    new_format = "%Y_%b_%d"
    new_date = date_obj.strftime(new_format)
    return new_date


def write_data(data, date: datetime.datetime):
    filename = f"{working_dir}\\{date.year}\\{date.month}\\{date.day}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # print(filename)
    # fields = ["Date", "Gallons"]
    with open(filename, "w", newline="") as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # writing data rows
        writer.writerows(data)


# for day in range(1, 20):
#     new_date = datetime.datetime(2024, 3, day)
#     new_format = "%Y-%b-%d"
#     new = new_date.strftime(new_format)
#     data = parse_daily_data(new)
#     # print(data)
#     write_data(data, new_date)


# data = parse_daily_data(current_date)
# print(data)
# print(get_month_day())
# write_data(data)
