from time import sleep
from selenium import webdriver
import os
import pandas as pd
import requests
from tabulate import tabulate
import json
from datetime import date

HAWK_URL = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=all&preset=all&globalSearch=HAWK&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
NORMAL_URL = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&pmComplianceMaxDate=todayOnly&pmComplianceMinDate=thisMonth&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
NEW_URL = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&globalSearch=hawks&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
CSV_FILE = "C:\\Users\\netwokz\\Desktop\\WorkOrderExport.csv"
CSV_PATH = "C:\\Users\\netwokz\\Desktop"

dt = date.today()
# Source
src = f'{CSV_PATH}WorkOrderExport.csv'
# Destination
dest = f'{CSV_PATH}hawk_pms_{dt}.csv'


AR_TECHS = ('CANDRUEL', 'EDURGR', 'MAJOSHN', 'WLNJON')


def download_to_csv():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    prefs = {'download.default_directory': CSV_PATH}
    options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    print("driver set to chrome")
    driver.get(HAWK_URL)
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
    sleep(15)
    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
    CSVButton.click()
    print("CSV Downloaded")
    sleep(1)


def send_webhook(my_data):
    # web_hook_link = 'https://hooks.slack.com/workflows/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'
    cbm_hook = "https://hooks.slack.com/workflows/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"
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"wo_data": my_data})
    response = requests.post(cbm_hook, headers=headers, data=data)
    print(response)


def rename_file():
    os.rename(src, dest)
    print("The file has been renamed.")


# download_to_csv()
if not os.path.exists(dest):
    download_to_csv()
    rename_file()

# df = pd.read_csv(dest)
# df = df.sort_values(by='Index', ascending=True)
# df = df.drop(columns=['PM Compliance Min Date', 'Scheduled End Date', 'Priority',
#              'Equipment Criticality', 'Equipment Alias', 'Type', 'Index', 'Equipment Description', 'Completed date'])

# # df = df[~df['Description'].str.contains('DAILY')]
# df = df[~df['Status'].str.contains('Completed')]
# df = df[~df['Status'].str.contains('Cancelled')]
# tab = (tabulate(df, tablefmt="pipe", headers="keys", showindex=False))
# # print(len(df.index))
# print(tab)

# if len(df.index) > 0:
#     send_webhook(tab)
