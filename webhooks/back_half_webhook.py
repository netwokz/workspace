from datetime import date, timedelta
import os
import pandas as pd
from tabulate import tabulate
import UTIL

EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority', 'Equipment Criticality',
                    'Equipment Alias', 'Equipment Description', 'Status', 'Equipment', 'Index']
EXCLUDED_TYPES = ['CBM', 'PR', 'CM', 'BRKD', 'FPM', 'SEV']
BHD_TECHS = ['AREAARON', 'VANBUC', 'ZDHARR', 'FELSOLON', 'ISAIACON',
             'JSONHU', 'JRRYCH', 'KKAMERJO', 'ANTOPLAC', 'LITTREDE']

BHN_TECHS = ['ADELALBA', 'AUSNMAJO', 'BUTLEEBR', 'RMGAB',
             'ACASJACO', 'REYESBJU', 'NATENEAL', 'JOVEROTL']

CSV_FILE = os.path.expanduser("~\\Documents\\WEBHOOK\\WorkOrderExport.csv")
CSV_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\")


def get_back_half_days():
    today = date.today()
    if today.weekday() == 0:
        start_of_week = today
        end_of_week = today + timedelta(days=2)
    elif today.weekday() == 1:
        start_of_week = today
        end_of_week = today + timedelta(days=1)
    elif today.weekday() == 2:
        start_of_week = today + timedelta(days=4)
        end_of_week = today + timedelta(days=7)
    elif today.weekday() == 3:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    elif today.weekday() == 4:
        start_of_week = today + timedelta(days=2)
        end_of_week = today + timedelta(days=5)
    elif today.weekday() == 5:
        start_of_week = today + timedelta(days=1)
        end_of_week = today + timedelta(days=4)
    elif today.weekday() == 6:
        start_of_week = today
        end_of_week = today + timedelta(days=3)
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
    return start, end


start, end = get_back_half_days()

# start = dates[0]
# end = dates[1]
if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)
UTIL.download_to_csv(start, end)


def parse_csv():
    df = pd.read_csv(CSV_FILE)

    for item in EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.loc[~df["Description"].str.contains("DAILY")]
    df = df.loc[~df["Type"].isin(EXCLUDED_TYPES)]
    df = df.loc[df["WO Owner"].isin(BHD_TECHS)]
    df = df.sort_values(by='Original PM due date', ascending=True)
    df.reset_index(inplace=True, drop=True)

    size = len(df.index)
    if size > 0:
        dataframe_chunk_size = 30
        list_df = [df[i:i+dataframe_chunk_size]
                   for i in range(0, len(df), dataframe_chunk_size)]
        for frame in list_df:
            tab = (tabulate(frame, tablefmt="pipe",
                   headers="keys", showindex=False))
            # send_webhook(tab)
            print(tab)


parse_csv()
