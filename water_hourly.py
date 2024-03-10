import csv
import datetime
import json
import os
from textwrap import indent

date = datetime.datetime.now()
date = date - datetime.timedelta(days=1)
new_format = "%m/%d/%Y"
current_date = date.strftime(new_format)

# current_date = "01/31/2024"


# import urllib library
from urllib.request import urlopen


def get_data_json(date):
    URL = f"https://beaz-p-ia-wb.itron-hosting.com/AnalyticsCustomerPortal_BEAZ_PROD/PortalServices/api/UsageData/Interval/?servicePointId=26329&accountId=988503-522366&skipHours=0&takeHours=24&endDate={date}"
    # store the response of URL
    response = urlopen(URL)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())
    # for item in data_json:
    # print(item)
    return data_json


def convert(datetime_str):
    # Example with the standard date and time format
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(datetime_str, date_format)
    # new_format = "%b %d, %Y"
    new_format = "%Y-%m-%d%H:%M:%S"
    new_date = date_obj.strftime(new_format)
    return new_date


def parse_daily_data(date):
    daily_data = get_data_json(date)
    daily_data_list = []
    for item in daily_data:
        if item["Usage"] is not None:
            usage = int((float(item["Usage"]) * 1000))
            if usage > 0:
                date = item["Date"]
                daily_data_list.append([date, usage])

    return daily_data_list


def get_month_day():
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(daily_data[-1]["Date"], date_format)
    new_format = "%Y_%b_%d"
    new_date = date_obj.strftime(new_format)
    return new_date


def write_data(data, date: datetime.datetime):
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "nov", "december"]
    displayMonth = months[date.month - 1]
    filename = f"C:\\Users\\deanejst\\Desktop\\csv_data\\{date.year}\\{displayMonth}\\{date.month}-{date.day}.csv"
    if os.path.exists(filename):
        return
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(filename)
    fields = ["Date", "Gallons"]
    with open(filename, "w", newline="") as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # writing headers (field names)
        writer.writerow(fields)

        # writing data rows
        writer.writerows(data)


for day in range(13, 31):
    new_date = datetime.datetime(2023, 11, day)
    new_format = "%d/%b/%Y"
    new = new_date.strftime(new_format)
    data = parse_daily_data(new)
    # print(data)
    write_data(data, new_date)


# data = parse_daily_data(current_date)
# print(current_date)
# print(get_month_day())
# write_data(data)
