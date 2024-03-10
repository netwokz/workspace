import csv
import datetime
import json
from textwrap import indent

date = datetime.datetime.now()
date = date - datetime.timedelta(days=1)
new_format = "%m/%d/%Y"
date = date.strftime(new_format)

# date = "01/31/2024"

# get daily totals
URL = f"https://beaz-p-ia-wb.itron-hosting.com/AnalyticsCustomerPortal_BEAZ_PROD/PortalServices/api/UsageData/Bundle/?accountId=988503-522366&servicepointid=26329&include=All&endDate={date}%2000:02:00%20AM&showMonthly=true"

# get hourly totals
# URL = f"https://beaz-p-ia-wb.itron-hosting.com/AnalyticsCustomerPortal_BEAZ_PROD/PortalServices/api/UsageData/Interval/?servicePointId=26329&accountId=988503-522366&skipHours=0&takeHours=24&endDate=2024-02-01"


# import urllib library
from urllib.request import urlopen

daily_data = ""


def get_data_json():
    # store the response of URL
    response = urlopen(URL)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())
    global daily_data
    daily_data = data_json[0]["DailyData"]["Detail"]
    return daily_data


def convert(datetime_str):
    # Example with the standard date and time format
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(datetime_str, date_format)
    # new_format = "%b %d, %Y"
    new_format = "%m/%d/%Y"
    new_date = date_obj.strftime(new_format)
    return new_date


def parse_daily_data():
    daily_data = get_data_json()
    daily_data_list = []
    for item in daily_data:
        if item["Usage"] is not None:
            usage = int((float(item["Usage"]) * 1000))
            date = convert(item["Date"])
            daily_data_list.append([date, usage])

    return daily_data_list


def get_month_day():
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_obj = datetime.datetime.strptime(daily_data[-1]["Date"], date_format)
    new_format = "%Y_%b"
    new_date = date_obj.strftime(new_format)
    return new_date


def write_data(data):
    name = get_month_day()
    filename = name + ".csv"
    fields = ["Date", "Gallons"]
    with open(filename, "w", newline="") as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # writing headers (field names)
        writer.writerow(fields)

        # writing data rows
        writer.writerows(data)


data = parse_daily_data()
# print(data)
# write_data(data)
