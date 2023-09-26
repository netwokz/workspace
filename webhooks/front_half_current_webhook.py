from datetime import date, timedelta
import os
import pandas as pd
from tabulate import tabulate
import UTIL


def get_front_half_days():
    today = date.today()
    print(today.weekday())
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


start, end = get_front_half_days()

if os.path.exists(UTIL.CSV_FILE):
    os.remove(UTIL.CSV_FILE)
UTIL.download_to_csv(start, end)


def parse_csv():
    df = pd.read_csv(UTIL.CSV_FILE)

    for item in UTIL.EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.loc[~df["Description"].str.contains("DAILY")]
    # df = df.loc[~df["Type"].isin(UTIL.EXCLUDED_TYPES)]
    df = df.loc[df["WO Owner"].isin(UTIL.FHD_TECHS)]
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
            # UTIL.send_webhook(UTIL.FHD_URL, tab)
            print(tab)
    print(f"Total number of WO's: {size}")


parse_csv()
