from datetime import date, timedelta
import os
from dotenv import dotenv_values
from time import sleep
from selenium import webdriver

dt = date.today()

secrets = dotenv_values(os.path.expanduser(
    "~\\Documents\\CODE\\workspace\\webhooks\\.env"))
USERNAME = secrets.get('username')
PASSWORD = secrets.get('password')


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
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
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
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
    return start, end


CSV_FILE = os.path.expanduser("~\\Documents\\WEBHOOK\\WorkOrderExport.csv")
CSV_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\")


def download_to_csv(start_date, end_date):
    NORMAL_URL = f"https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&dueDate=customDateRange,{start_date},{end_date}&primaryOwnerSort=asc,1&pmComplianceMaxDateSort=asc,2"
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
