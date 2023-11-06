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
def get_week_end(day=dt):
    my_dt_trunc = day
    # print(my_dt_trunc)
    # print(my_dt_trunc.weekday())
    if my_dt_trunc.weekday() == 6:
        end_of_week = my_dt_trunc + timedelta(days = 6)
    else:
        end_of_week = my_dt_trunc + timedelta(days = (5 - my_dt_trunc.weekday()))
    # print(end_of_week)  
    return end_of_week.strftime('%Y-%m-%d')

def get_week_start(day=dt):
    my_dt_trunc = day
    # print(my_dt_trunc)
    # print(my_dt_trunc.weekday())
    if my_dt_trunc.weekday() == 6:
        start_of_week = my_dt_trunc
    elif my_dt_trunc.weekday() == 0:
        start_of_week = my_dt_trunc - timedelta(days = 1)
    else:
        start_of_week = my_dt_trunc - timedelta(days = my_dt_trunc.weekday() + 1)
    # print(start_of_week)  
    return start_of_week.strftime('%Y-%m-%d')

END_OF_WEEK = get_week_end()
START_OF_WEEK = get_week_start()
CSV_FILE = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\WorkOrderExport.csv"
CSV_PATH = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\"
DOWNLOAD_FOLDER = ""

URL = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&pmComplianceMaxDate=customDateRange,{START_OF_WEEK},{END_OF_WEEK}&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/workflows/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"
SLACK_VARIABLE = "wo_id"

COLUMS_TO_DROP = ['Index', 'PM Compliance Min Date', 'Scheduled End Date', 'Priority',
                  'Equipment Criticality', 'Equipment Alias', 'Type', 'Equipment Description', 'Completed date']
# DESCRIPTION_EXCLUSION_LIST = ["DAILY"]
DESCRIPTION_EXCLUSION_LIST = []
STATUS_EXCLUSION_LIST = ["Remedy Request"]

chromedriver_autoinstaller.install(cwd=True)

AR_TECHS = ('CANDRUEL', 'EDURGR', 'MAJOSHN', 'WLNJON')
# Source
src = f'{CSV_PATH}WorkOrderExport.csv'
# Destination
dest = f'{CSV_PATH}hawk_pms_{dt}.csv'

def get_download_folder():
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads\\"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads/"
    return DOWNLOAD_FOLDER
    # print(DOWNLOAD_FOLDER)

def pull_wo_to_csv():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    prefs = {'download.default_directory': DOWNLOAD_FOLDER}
    options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    print("driver set to chrome")
    driver.get(URL)
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
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({SLACK_VARIABLE: my_data})
    response = requests.post(SLACK_WEBHOOK_URL, headers=headers, data=data)
    print(response)

def rename_file():
    os.rename(src, dest)
    print("The file has been renamed.")

def do_workflow():
    df = pd.read_csv(os.path.join(get_download_folder(), "WorkOrderExport.csv"))
    df = df.sort_values(by='Index', ascending=True)
    df = df.drop(columns=COLUMS_TO_DROP)
    for item in DESCRIPTION_EXCLUSION_LIST:
        df = df[~df['Description'].str.contains(item)]
    for item in STATUS_EXCLUSION_LIST:
        df = df[~df['Status'].str.contains(item)]
    tab = (tabulate(df, tablefmt="orgtbl ", headers="keys", showindex=False))
    print(tab)
    # Send webhook if there is any data available
    # if len(df.index) > 0:
    # send_Webhook(tab)


# my_date = date(year=2023, month=5, day=9)
# get_week_end(my_date)
# get_week_end()

# get_week_start(my_date)

# print(URL)

if not os.path.exists(os.path.join(get_download_folder(), "WorkOrderExport.csv")):
    # print("File not found")
    pull_wo_to_csv()
    pass

do_workflow()
