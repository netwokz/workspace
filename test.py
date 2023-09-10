from datetime import date
import db_helper
import pandas as pd
from EzrmeUtils import DownloadUtils
from tabulate import tabulate
import json
import requests

dt = date.today()

my_db = db_helper.WODBHelper("C:\\Users\\deanejst\\tote_stacker.db")
db_table_name = my_db.TABLE_NAME
my_path = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\WorkOrderExport.csv"
EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Scheduled End Date', 'Priority', 'Equipment Criticality',
                    'Equipment Alias', 'Equipment Description', 'Completed date', 'Scheduled Start Date', 'Status', 'Equipment', 'Index']
CBM_URL = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&type=CBM"
mine = DownloadUtils


def send_webhook(my_data):
    URL = "https://hooks.slack.com/workflows/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"  # FHD Webhook URL
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    print(response)


def iterate_data(data_frame):
    for index in data_frame.index:
        if not my_db.has_entry(str(data_frame["Workorder ID"][index])):
            my_db.add_entry(str(data_frame["Workorder ID"][index]), data_frame["Description"][index], data_frame["Type"][index], data_frame["WO Owner"]
                            [index], data_frame["PM Compliance Max Date"][index], data_frame["Link"][index])
            # send_webhook(data_frame.iloc["Workorder ID"][index])

def load_data_from_db():
    new_data = my_db.get_entries()
    new_data.columns = ["Workorder ID", "Description",
                        "Type", "WO Owner", "PM Compliance Max Date", "Link"]
    tab = tabulate(new_data, tablefmt="pipe", headers="keys", showindex=False)
    # print(tab)


if dt.weekday == 6:
    my_db.delete_db()

# mine.download_to_csv(CBM_URL)

if not my_db.check_db():
    my_db.init_db()
my_db.does_table_exist()

df = pd.read_csv(my_path)
df = df.sort_values(by='PM Compliance Max Date', ascending=True)
df = df.drop(columns=EXCLUDED_COLUMNS)
df = df.loc[~df["Description"].str.contains("Hawk")]
tab = (tabulate(df, tablefmt="pipe", headers="keys", showindex=False))
# print(tab)
# print(len(df.index))

iterate_data(df)
load_data_from_db()
