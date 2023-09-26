import os
import pandas as pd
from tabulate import tabulate
import UTIL


CBM_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\")
CBM_FILE = os.path.expanduser(
    "~\\Documents\\WEBHOOK\\cbm\\WorkOrderExport.csv")

if os.path.exists(CBM_FILE):
    os.remove(CBM_FILE)
UTIL.get_cbm()


def parse_csv():
    df = pd.read_csv(CBM_FILE)

    for item in UTIL.EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
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
