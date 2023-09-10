from time import sleep
from selenium import webdriver
import os
import pandas as pd
import requests
from tabulate import tabulate
import json
import chromedriver_autoinstaller
from datetime import date, timedelta


dt = date.today()

def get_week_start(day=dt):
    my_dt_trunc = day
    if my_dt_trunc.weekday() == 6:
        start_of_week = my_dt_trunc + timedelta(days = 3)
    elif my_dt_trunc.weekday() == 0:
        start_of_week = my_dt_trunc + timedelta(days = 2)
    elif my_dt_trunc.weekday() == 1:
        start_of_week = my_dt_trunc + timedelta(days = 1)
    else:
        start_of_week = my_dt_trunc
    return start_of_week.strftime('%Y-%m-%d')

def get_week_end(day=dt):
    my_dt_trunc = day
    if my_dt_trunc.weekday() == 6:
        end_of_week = my_dt_trunc + timedelta(days = 6)
    else:
        end_of_week = my_dt_trunc + timedelta(days = (5 - my_dt_trunc.weekday()))
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

chromedriver_autoinstaller.install(cwd=True)

EXCLUDED_COLUMNS = ['PM Compliance Min Date', 'Scheduled End Date', 'Priority', 'Equipment Criticality', 'Equipment Alias', 'Index', 'Equipment Description', 'Completed date', 'Scheduled Start Date', 'Status', 'Equipment']
FHD_TECHS = ['ASHPFAF', 'EDURGR', 'GSALAEDW', 'HERTAJU', 'KIECLAR', 'HRYATAYL', 'RMGAB', 'CLARKSSI', 'SAUVRGA', 'WLNJON', 'DEANEJST', 'DUNHCHAS']
ALLOWED_TYPES = ['CBM', 'PR', 'CM', 'BRKD', 'FPM', 'SEV']

def download_to_csv():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
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

def send_webhook(my_data):
    # URL = "https://hooks.slack.com/workflows/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" # CBM Channel
    URL = "https://hooks.slack.com/workflows/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" # My Message
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(URL, headers=headers, data=data)
    print(response)

def rename_file():
    os.rename(src, dest)
    print("The file has been renamed.")

if not os.path.exists(src):
    download_to_csv()
    # rename_file()

df = pd.read_csv(src)
df = df.sort_values(by='Index', ascending=True)
df = df.drop(columns=EXCLUDED_COLUMNS)
df = df.loc[~df["Type"].isin(ALLOWED_TYPES)]
df1 = df.loc[df["WO Owner"].isin(FHD_TECHS)]
tab = (tabulate(df1, tablefmt="pipe", headers="keys", showindex=False))
# print(len(df.index))
df1.to_csv(CSV_PATH + 'edited.csv', index=False)
print(tab)
print(len(df1.index))

if len(df1.index) > 0:
    send_webhook(tab)
