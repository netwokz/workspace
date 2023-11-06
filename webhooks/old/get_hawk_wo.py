from time import sleep
from selenium import webdriver
import os
import pandas as pd
import requests
from tabulate import tabulate
import json
import chromedriver_autoinstaller

EZ_RME_URL = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?customPreset=allPM&preset=allPM&pmComplianceMaxDate=todayOnly&organizationId=GYR1&status=S,RR,RS,IP,R"
SLACK_WEB_HOOK_URL = 'https://hooks.slack.com/workflows/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'
DOWNLOAD_FOLDER = ""
FILE_PATH = 'C:\\Users\\netwokz\\Documents\\'
SLACK_VARIABLE = "PM"
COLUMS_TO_DROP = ['Organization', 'Original PM due date', 'Index', 'PM Compliance Min Date', 'Scheduled End Date', 'Priority',
                  'Shift ID', 'Equipment Criticality', 'Equipment Alias', 'Type', 'Equipment Description', 'Precision WO', 'Created By', 'Completed date']
# DESCRIPTION_EXCLUSION_LIST = ["DAILY"]
DESCRIPTION_EXCLUSION_LIST = []

EMAIL = "gramigu@amazon.com"
PASSWORD = "123456"

chromedriver_autoinstaller.install(cwd=True)


def get_download_folder():
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads\\"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads/"
    return DOWNLOAD_FOLDER
    # print(DOWNLOAD_FOLDER)


def pull_wo_to_csv():
    # Setup chrome browser
    options = webdriver.ChromeOptions()

    # Hide browser window
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--incognito")
    prefs = {'download.default_directory': DOWNLOAD_FOLDER}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    # Load URL
    driver.get(EZ_RME_URL)
    sleep(1)

    # Get "Sign In As Button"
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')")
    SignInASButton.click()
    sleep(3)

    # Get Email input box
    email = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    # Enter Email
    email.send_keys(EMAIL)
    sleep(5)

    # Get Email input box
    passwd = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    # Enter Password
    passwd.send_keys(PASSWORD)
    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')")
    sign_on.click()
    sleep(6)

    # Delete old file if it exists.
    if os.path.isfile(DOWNLOAD_FOLDER + "WorkOrderExport.csv"):
        os.remove(DOWNLOAD_FOLDER + "WorkOrderExport.csv")

    # Get "Export to CSV" Button
    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
    CSVButton.click()
    sleep(5)


def send_Webhook(tab_data):
    headers = {
        'Content-Type': 'application/json',
    }
    contents = json.dumps({SLACK_VARIABLE: tab_data})
    response = requests.post(
        SLACK_WEB_HOOK_URL, headers=headers, data=contents)
    print(response)


def do_workflow():
    df = pd.read_csv(FILE_PATH + "WorkOrderExport.csv")
    df = df.sort_values(by='Index', ascending=True)
    df = df.drop(columns=COLUMS_TO_DROP)
    for item in DESCRIPTION_EXCLUSION_LIST:
        df = df[~df['Description'].str.contains(item)]
    tab = (tabulate(df, tablefmt="orgtbl ", headers="keys", showindex=False))
    print(tab)
    # Send webhook if there is any data available
    # if len(df.index) > 0:
    # send_Webhook(tab)


if not os.path.exists(os.path.join(get_download_folder(), "WorkOrderExport.csv")):
    # print("File not found")
    pull_wo_to_csv()
    pass

# do_workflow()
