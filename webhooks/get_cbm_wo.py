import os

import pandas as pd
import UTIL
from tabulate import tabulate

URL_MHE = "https://hooks.slack.com/workflows/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"  # variable = data
URL_AR = "https://hooks.slack.com/workflows/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"  # variable = data

CBM_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\")
CBM_FILE = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\WorkOrderExport.csv")

AR_TAGS = ["CEL", "Drive", "Fid"]

if os.path.exists(CBM_FILE):
    os.remove(CBM_FILE)
UTIL.get_cbm()


def parse_csv():
    df = pd.read_csv(CBM_FILE)

    for item in UTIL.EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.loc[~df["Description"].str.contains("CEL|Drive|Fid")]
    df = df.sort_values(by="Original PM due date", ascending=True)
    df.reset_index(inplace=True, drop=True)

    size = len(df.index)
    if size > 0:
        dataframe_chunk_size = 30
        list_df = [df[i : i + dataframe_chunk_size] for i in range(0, len(df), dataframe_chunk_size)]
        for frame in list_df:
            tab = tabulate(frame, tablefmt="pipe", headers="keys", showindex=False)
            UTIL.send_webhook(URL_MHE, tab)
            print(tab)
    print(f"Total number of WO's: {size}")


def parse_csv_for_ar():
    df = pd.read_csv(CBM_FILE)

    for item in UTIL.EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.loc[df["Description"].str.contains("CEL|Drive|Fid")]
    df = df.sort_values(by="Original PM due date", ascending=True)
    df.reset_index(inplace=True, drop=True)

    size = len(df.index)
    if size > 0:
        dataframe_chunk_size = 30
        list_df = [df[i : i + dataframe_chunk_size] for i in range(0, len(df), dataframe_chunk_size)]
        for frame in list_df:
            tab = tabulate(frame, tablefmt="pipe", headers="keys", showindex=False)
            UTIL.send_webhook(URL_AR, tab)
            print(tab)
    print(f"Total number of WO's: {size}")


parse_csv()
parse_csv_for_ar()
