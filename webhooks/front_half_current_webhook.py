from datetime import date, timedelta
from download_wo import download_to_csv
import os
import pandas as pd
from tabulate import tabulate

EXCLUDED_COLUMNS = ['Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority', 'Equipment Criticality',
                    'Equipment Alias', 'Equipment Description', 'Status', 'Equipment', 'Index']

EXCLUDED_TYPES = ['CBM', 'PR', 'CM', 'BRKD', 'FPM', 'SEV']

FHD_TECHS = ['ASHPFAF', 'GSALAEDW', 'IXTAJ', 'HERTAJU',
             'KIECLAR', 'WINNEMIC', 'HRYATAYL', 'CLARKSSI', 'FETICHER']

FHN_TECHS = ['CANDRUEL', 'QMOYCHRI', 'JOPADEYI', 'WLNJON',
             'JCSTROZ', 'MPEREZF', 'SHATPRAT', 'STUARTYL']

CSV_FILE = os.path.expanduser("~\\Documents\\WEBHOOK\\WorkOrderExport.csv")
CSV_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\")


# def get_front_half_days():
#     today = date.today()
#     if today.weekday() == 6:
#         start_of_week = today + timedelta(days=3)
#         end_of_week = today + timedelta(days=6)
#     elif today.weekday() == 0:
#         start_of_week = today + timedelta(days=2)
#         end_of_week = today + timedelta(days=(5 - today.weekday()))
#     elif today.weekday() == 1:
#         start_of_week = today + timedelta(days=1)
#         end_of_week = today + timedelta(days=(5 - today.weekday()))
#     else:
#         start_of_week = today
#         end_of_week = today + timedelta(days=(5 - today.weekday()))
#     start = start_of_week.strftime('%Y-%m-%d')
#     end = end_of_week.strftime('%Y-%m-%d')
#     return start, end

def get_front_half_days():
    today = date.today()
    print(today.isoweekday)
    if today.isoweekday() == 6:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
    return start, end


print(get_front_half_days())

start, end = get_front_half_days()

# if os.path.exists(CSV_FILE):
#     os.remove(CSV_FILE)
# download_to_csv(start, end)


def parse_csv():
    df = pd.read_csv(CSV_FILE)

    for item in EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.loc[~df["Description"].str.contains("DAILY")]
    df = df.loc[~df["Type"].isin(EXCLUDED_TYPES)]
    df = df.loc[df["WO Owner"].isin(FHD_TECHS)]
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
    print(f"Total number of WO's: {size}")


parse_csv()
