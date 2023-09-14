from time import sleep
from selenium import webdriver
import os
import pandas as pd
import requests
from tabulate import tabulate
import json
from datetime import date, timedelta
from dotenv import dotenv_values


dt = date.today()

secrets = dotenv_values(
    "C:\\Users\\deanejst\\Documents\\CODE\\workspace\\webhooks\\.env")
USERNAME = secrets.get('username')
PASSWORD = secrets.get('password')


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

MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data
WEBHOOK_FAILED_MSG = f"get_week_ending_max webhook failed to send"

NORMAL_URL = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&dueDate=customDateRange,{START_OF_WEEK},{END_OF_WEEK}&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
CSV_FILE = "C:\\Users\\gyr1-flowdesk\\Documents\\WO_CSV\\max_webhook\\WorkOrderExport.csv"
CSV_PATH = 'C:\\Users\\gyr1-flowdesk\\Documents\\WO_CSV\\max_webhook\\'

USERNAME = "gramigu@amazon.com"
PASSWORD = "123456"

dt = date.today()
# Source
src = f'{CSV_PATH}WorkOrderExport.csv'
# Destination
dest = f'{CSV_PATH}hawk_pms_{dt}.csv'

# EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Scheduled End Date', 'Priority', 'Equipment Criticality', 'Equipment Alias', 'Equipment Description', 'Completed date', 'Scheduled Start Date', 'Status', 'Equipment', 'Original PM due date', 'Organization', 'Precision WO', 'Created By', 'Shift ID', 'Index']
EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Equipment Alias', 'Equipment Description', 'Completed date',
                    'Scheduled Start Date', 'Status', 'Equipment', 'Original PM due date', 'Created By', 'Shift ID', 'Index']
FHD_TECHS = ['ASHPFAF', 'EDURGR', 'GSALAEDW', 'HERTAJU', 'KIECLAR',
             'HRYATAYL', 'RMGAB', 'CLARKSSI', 'SAUVRGA', 'WLNJON', 'DEANEJST', 'DUNHCHAS']
ALLOWED_TYPES = ['CBM', 'PR', 'CM', 'BRKD', 'FPM', 'SEV']


def download_to_csv():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    prefs = {'download.default_directory': CSV_PATH}
    options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    print("driver set to chrome")
    driver.get(NORMAL_URL)
    print("Page LOADED")
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')")
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(3)

    email = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    sleep(1)
    email.send_keys(USERNAME)
    sleep(5)

    passwd = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    passwd.send_keys(PASSWORD)
    sleep(5)

    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')")
    sign_on.click()

    sleep(1)
    print("Sign On CLICKED")
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
    CSVButton.click()
    print("CSV Downloaded")
    sleep(10)


def send_fail_notification():
    URL = MY_TEST_URL  # FHD Webhook URL
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": WEBHOOK_FAILED_MSG})
    response = requests.post(URL, headers=headers, data=data)
    print(response.status_code)


def send_webhook(my_data):
    URL = "https://hooks.slack.com/workflows/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"  # FHD Webhook URL
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    if response.status_code != 200:
        send_fail_notification()


def rename_file():
    os.rename(src, dest)
    print("The file has been renamed.")


if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)
download_to_csv()

df = pd.read_csv(CSV_FILE)
df = df.sort_values(by='Original PM due date', ascending=True)
for item in EXCLUDED_COLUMNS:
    if item in df:
        df = df.drop(columns=item)
df = df.loc[~df["Type"].isin(ALLOWED_TYPES)]
df = df.loc[~df["Description"].str.contains('DAILY')]
df = df.loc[df["WO Owner"].isin(FHD_TECHS)]
df.reset_index(drop=True, inplace=True)

size = len(df.index)

if size > 0:
    dataframe_chunk_size = 30
    list_df = [df[i:i+dataframe_chunk_size]
               for i in range(0, len(df), dataframe_chunk_size)]
    for dataframe in list_df:
        tab = (tabulate(dataframe, tablefmt="pipe",
               headers="keys", showindex=False))
        # send_webhook(tab)
        print(tab)
