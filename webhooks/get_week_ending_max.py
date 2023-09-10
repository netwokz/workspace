from time import sleep
from selenium import webdriver
import os
import pandas as pd
import requests
from tabulate import tabulate
import json
from datetime import date, timedelta

ALI_URL = "https://hooks.slack.com/workflows/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"  # variable = data
SAUL_URL = "https://hooks.slack.com/workflows/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"  # variable = data
CBM_URL = "https://hooks.slack.com/workflows/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"  # variable = Content
FHD_URL = "https://hooks.slack.com/workflows/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"  # variable = data
BHN_URL = "https://hooks.slack.com/workflows/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"  # variable = Content
MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data
WEBHOOK_FAILED_MSG = f"get_week_ending_max webhook failed to send"

dt = date.today()


def get_week_start(day=dt):
    my_dt_trunc = day
    if my_dt_trunc.weekday() == 6:
        start_of_week = my_dt_trunc + timedelta(days=3)
    elif my_dt_trunc.weekday() == 0:
        start_of_week = my_dt_trunc + timedelta(days=2)
    elif my_dt_trunc.weekday() == 1:
        start_of_week = my_dt_trunc + timedelta(days=1)
    else:
        start_of_week = my_dt_trunc
    return start_of_week.strftime('%Y-%m-%d')


def get_week_end(day=dt):
    my_dt_trunc = day
    if my_dt_trunc.weekday() == 6:
        end_of_week = my_dt_trunc + timedelta(days=6)
    else:
        end_of_week = my_dt_trunc + timedelta(days=(5 - my_dt_trunc.weekday()))
    return end_of_week.strftime('%Y-%m-%d')


END_OF_WEEK = get_week_end()
START_OF_WEEK = get_week_start()

NORMAL_URL = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&pmComplianceMaxDate=customDateRange,{START_OF_WEEK},{END_OF_WEEK}&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
CSV_FILE = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\WorkOrderExport.csv"
CSV_PATH = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\"

dt = date.today()
# Source
src = f'{CSV_PATH}WorkOrderExport.csv'
# Destination
dest = f'{CSV_PATH}hawk_pms_{dt}.csv'


EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Scheduled End Date', 'Priority', 'Equipment Criticality',
                    'Equipment Alias', 'Equipment Description', 'Completed date', 'Scheduled Start Date', 'Status', 'Equipment', 'Index']
FHD_TECHS = ['ASHPFAF', 'EDURGR', 'GSALAEDW', 'HERTAJU', 'KIECLAR',
             'HRYATAYL', 'RMGAB', 'CLARKSSI', 'SAUVRGA', 'WLNJON', 'DEANEJST', 'DUNHCHAS']
EXCLUDED_TYPES = ['CBM', 'PR', 'CM', 'BRKD', 'FPM', 'SEV']


def download_to_csv():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    prefs = {'download.default_directory': CSV_PATH}
    options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    print("driver set to chrome")
    driver.get(NORMAL_URL)
    print("Page LOADED")
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')")
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(1)
    SingleSignOnButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#sso-login').shadowRoot.querySelector('#button')")
    SingleSignOnButton.click()
    print("Single Sign On CLICKED")
    sleep(5)
    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
    CSVButton.click()
    print("CSV Downloaded")
    sleep(5)


def send_fail_notification():
    URL = MY_TEST_URL  # FHD Webhook URL
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": WEBHOOK_FAILED_MSG})
    response = requests.post(URL, headers=headers, data=data)
    print(response.status_code)


def send_webhook(my_data):
    URL = FHD_URL  # FHD Webhook URL
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    if response.status_code != 200:
        send_fail_notification()
    # print(response.status_code)


def rename_file():
    os.rename(src, dest)
    print("The file has been renamed.")


# if os.path.exists(CSV_FILE):
#     os.remove(CSV_FILE)
# download_to_csv()

df = pd.read_csv(CSV_FILE)
df = df.sort_values(by='PM Compliance Max Date', ascending=True)
for item in EXCLUDED_COLUMNS:
    if item in df.columns:
        df = df.drop(columns=item)
df = df.loc[~df["Description"].str.contains("DAILY")]
df = df.loc[~df["Type"].isin(EXCLUDED_TYPES)]
df = df.loc[df["WO Owner"].isin(FHD_TECHS)]
df.reset_index(inplace=True, drop=True)

size = len(df.index)
if size > 0:
    dataframe_chunk_size = 30

    list_df = [df[i:i+dataframe_chunk_size]
               for i in range(0, len(df), dataframe_chunk_size)]
    for frame in list_df:
        tab = (tabulate(frame, tablefmt="pipe", headers="keys", showindex=False))
        send_webhook(tab)
        # print(tab)
        # print("\n")

# print(len(df.index))
# df.to_csv(CSV_PATH + 'edited.csv', index=False)
