import json
import os
from datetime import date, timedelta
from time import sleep

import pyshorteners
import requests
from dotenv import dotenv_values
from selenium import webdriver

dt = date.today()
type_tiny = pyshorteners.Shortener()

secrets = dotenv_values(os.path.expanduser("~\\Documents\\CODE\\workspace\\webhooks\\.env"))
USERNAME = secrets.get("username")
PASSWORD = secrets.get("password")

CSV_FILE = os.path.expanduser("~\\Documents\\WEBHOOK\\WorkOrderExport.csv")
CSV_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\")
CBM_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\")

ALI_URL = "https://hooks.slack.com/workflows/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"  # variable = data
SAUL_URL = "https://hooks.slack.com/workflows/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"  # variable = data
CBM_URL = "https://hooks.slack.com/workflows/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"  # variable = data
FHD_URL = "https://hooks.slack.com/workflows/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"  # variable = data
BHN_URL = "https://hooks.slack.com/workflows/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"  # variable = Content
MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data
WEBHOOK_FAILED_MSG = f"get_week_ending_max webhook failed to send"

EXCLUDED_COLUMNS = [
    "Type",
    "Organization",
    "Precision WO",
    "Created By",
    "Shift ID",
    "PM Compliance Min Date",
    "Scheduled Start Date",
    "Scheduled End Date",
    "Completed date",
    "Priority",
    "Equipment Criticality",
    "Equipment Alias",
    "Equipment Description",
    "Status",
    "Equipment",
    "Index",
]


FHD_TECHS = ["JNEAUS", "ASHPFAF", "GSALAEDW", "IXTAJ", "HERTAJU", "KIECLAR", "WINNEMIC", "HRYATAYL", "CLARKSSI", "AUSNMAJO", "DEANEJST", "SAUVRGA"]

FHN_TECHS = ["CANDRUEL", "QMOYCHRI", "JOPADEYI", "WLNJON", "JCSTROZ", "MPEREZF", "SHATPRAT", "STUARTYL"]

BHD_TECHS = ["AREAARON", "VANBUC", "ZDHARR", "FELSOLON", "ISAIACON", "JSONHU", "JRRYCH", "KKAMERJO", "ANTOPLAC", "LITTREDE"]

BHN_TECHS = ["ADELALBA", "AUSNMAJO", "BUTLEEBR", "RMGAB", "ACASJACO", "REYESBJU", "NATENEAL", "JOVEROTL"]

FHD_CSX_TECHS = ["GEMCKEAG", "BREADJ", "SAUVRGA", "DEANEJST", "AHUERTAJ"]

EXCLUDED_TYPES = ["CBM", "PR", "CM", "BRKD", "FPM", "SEV"]


def download_to_csv(start_date, end_date):
    NORMAL_URL = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&dueDate=customDateRange,{start_date},{end_date}&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    # prefs = {'download.default_directory': CSV_PATH}
    # options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    driver.get(NORMAL_URL)
    params = {"cmd": "Page.setDownloadBehavior", "params": {"behavior": "allow", "downloadPath": CSV_PATH}}
    driver.command_executor._commands["send_command"] = ("POST", "/session/$sessionId/chromium/send_command")
    driver.execute("send_command", params)
    print("driver set to chrome")
    driver.get(NORMAL_URL)
    print("Page LOADED")
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')"
    )
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(3)

    email = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    sleep(1)
    email.send_keys(USERNAME)
    sleep(5)

    passwd = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    passwd.send_keys(PASSWORD)
    sleep(5)

    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')"
    )
    sign_on.click()

    sleep(1)
    print("Sign On CLICKED")
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')"
    )
    CSVButton.click()
    print("CSV Downloaded")
    sleep(10)


def get_current_wo(date):
    url = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&dueDate=customDateRange,2023-11-05,2023-11-05"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    # prefs = {
    #     "download.default_directory": CBM_PATH,
    #     "savefile.default_directory": CBM_PATH
    # }
    # options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # need to do this once instance has started
    params = {"cmd": "Page.setDownloadBehavior", "params": {"behavior": "allow", "downloadPath": CBM_PATH}}
    driver.command_executor._commands["send_command"] = ("POST", "/session/$sessionId/chromium/send_command")
    driver.execute("send_command", params)
    print("driver set to chrome")
    driver.get(url)
    print("Page LOADED")
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')"
    )
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(3)

    email = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    sleep(1)
    email.send_keys(USERNAME)
    sleep(5)

    passwd = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    passwd.send_keys(PASSWORD)
    sleep(5)

    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')"
    )
    sign_on.click()

    sleep(1)
    print("Sign On CLICKED")
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')"
    )
    CSVButton.click()
    print("CSV Downloaded")
    sleep(10)


def get_cbm():
    url = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&type=CBM"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    # prefs = {
    #     "download.default_directory": CBM_PATH,
    #     "savefile.default_directory": CBM_PATH
    # }
    # options.add_experimental_option('prefs', prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # need to do this once instance has started
    params = {"cmd": "Page.setDownloadBehavior", "params": {"behavior": "allow", "downloadPath": CBM_PATH}}
    driver.command_executor._commands["send_command"] = ("POST", "/session/$sessionId/chromium/send_command")
    driver.execute("send_command", params)
    print("driver set to chrome")
    driver.get(url)
    print("Page LOADED")
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')"
    )
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(3)

    email = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    sleep(1)
    email.send_keys(USERNAME)
    sleep(5)

    passwd = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    passwd.send_keys(PASSWORD)
    sleep(5)

    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')"
    )
    sign_on.click()

    sleep(1)
    print("Sign On CLICKED")
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')"
    )
    CSVButton.click()
    print("CSV Downloaded")
    sleep(10)


def get_all_csv(user):
    url = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2&primaryOwner={user}"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    prefs = {"download.default_directory": CSV_PATH}
    options.add_experimental_option("prefs", prefs)
    print("options added")
    driver = webdriver.Chrome(options=options)
    print("driver set to chrome")
    driver.get(url)
    print("Page LOADED")
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')"
    )
    SignInASButton.click()
    print("Sign On CLICKED")
    sleep(3)

    email = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#user-id')")
    email.click()
    sleep(1)
    email.send_keys(USERNAME)
    sleep(5)

    passwd = driver.execute_script("return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
    passwd.click()
    passwd.send_keys(PASSWORD)
    sleep(5)

    sign_on = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')"
    )
    sign_on.click()

    sleep(1)
    print("Sign On CLICKED")
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')"
    )
    CSVButton.click()
    print("CSV Downloaded")
    sleep(10)


def get_front_half_days(today):
    if today.weekday() == 6:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    elif today.weekday() == 0:
        start_of_week = today + timedelta(days=2)
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    elif today.weekday() == 1:
        start_of_week = today + timedelta(days=1)
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    else:
        start_of_week = today
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    start = start_of_week.strftime("%Y-%m-%d")
    end = end_of_week.strftime("%Y-%m-%d")
    return start, end


def get_back_half_days(today):
    if today.weekday() == 0:
        start_of_week = today
        end_of_week = today + timedelta(days=2)
    elif today.weekday() == 1:
        start_of_week = today
        end_of_week = today + timedelta(days=1)
    elif today.weekday() == 2:
        start_of_week = today + timedelta(days=4)
        end_of_week = today + timedelta(days=7)
    elif today.weekday() == 3:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    elif today.weekday() == 4:
        start_of_week = today + timedelta(days=2)
        end_of_week = today + timedelta(days=5)
    elif today.weekday() == 5:
        start_of_week = today + timedelta(days=1)
        end_of_week = today + timedelta(days=4)
    elif today.weekday() == 6:
        start_of_week = today
        end_of_week = today + timedelta(days=3)
    start = start_of_week.strftime("%Y-%m-%d")
    end = end_of_week.strftime("%Y-%m-%d")
    return start, end


def send_fail_notification():
    URL = MY_TEST_URL  # FHD Webhook URL
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps({"data": WEBHOOK_FAILED_MSG})
    response = requests.post(URL, headers=headers, data=data)
    # print(response.status_code)


def send_webhook(url, my_data):
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps({"data": my_data})
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.status_code != 200:
        send_fail_notification()
