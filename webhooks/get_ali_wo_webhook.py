from datetime import date, timedelta
import os
import pandas as pd
from tabulate import tabulate
import pyshorteners
import UTIL

type_tiny = pyshorteners.Shortener()

# if os.path.exists(CSV_FILE):
#     os.remove(CSV_FILE)
# get_all_csv("AHUERTAJ")


def parse_csv():
    df = pd.read_csv(UTIL.CSV_FILE)
    for link in df['Link']:
        df['Link'] = df['Link'].replace([link], type_tiny.tinyurl.short(link))
    for item in UTIL.EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.sort_values(by='Original PM due date', key=pd.to_datetime)
    df.reset_index(inplace=True, drop=True)

    size = len(df.index)
    if size > 0:
        dataframe_chunk_size = 30
        list_df = [df[i:i+dataframe_chunk_size]
                   for i in range(0, len(df), dataframe_chunk_size)]
        for frame in list_df:
            tab = (tabulate(frame, tablefmt="pipe",
                   headers="keys", showindex=False))
            UTIL.send_webhook(UTIL.ALI_URL, tab)
            print(tab)
    print(f"Total number of WO's: {size}")


parse_csv()
