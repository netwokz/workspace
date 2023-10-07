from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import pandas as pd
import os
import numpy as np
from selenium import webdriver
from time import sleep
from tabulate import tabulate
import json
import requests

Base = declarative_base()
EXCLUDED_COLUMNS = ['Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority',
                    'Status', 'Index']
FINAL_EXCLUDED_COLUMNS = ['Equipment Criticality', 'Equipment Alias', 'Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority',
                          'Equipment Description', 'Status', 'Index']
CBM_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\")
# CBM_FILE = os.path.expanduser(
#     "~\\Documents\\WEBHOOK\\cbm\\WorkOrderExport.csv")
CBM_FILE = os.path.expanduser(
    "~\\CODE\\workspace\\python\\wo_database\\WorkOrderExport.csv")
secrets = dotenv_values(os.path.expanduser(
    "~\\Documents\\CODE\\workspace\\webhooks\\.env"))
USERNAME = secrets.get('username')
PASSWORD = secrets.get('password')

MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data
URL = "https://hooks.slack.com/workflows/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"
WEBHOOK_FAILED_MSG = f"get_cbm_workorders webhook failed to send"


class Workorder(Base):
    __tablename__ = 'workorders'

    wo_id = Column('Workorder ID', String, primary_key=True)
    wo_desc = Column('Description', String)
    wo_owner = Column('WO Owner', String)
    wo_due_date = Column('Original PM due date', String)
    wo_link = Column('Link', String)
    wo_type = Column('Type', String)
    wo_equip = Column('Equipment', String)

    def __init__(self, wo_item):
        self.wo_id = wo_item[0]
        self.wo_desc = wo_item[1]
        self.wo_type = wo_item[2]
        self.wo_equip = wo_item[3]
        self.wo_owner = wo_item[4]
        self.wo_due_date = wo_item[5]
        self.wo_link = wo_item[6]

    def get_id(self):
        return self.wo_id

    def get_df_data(self):
        wo_dict = {
            "Workorder ID": self.wo_id,
            "Description": self.wo_desc,
            "Type": self.wo_type,
            "Equipment": self.wo_equip,
            "WO Owner": self.wo_owner,
            "Original PM due date": self.wo_due_date,
            "Link": self.wo_link
        }
        return wo_dict

    def __repr__(self):
        return f"wo_id: {self.wo_id}, wo_owner: {self.wo_owner}, wo_equip {self.wo_equip}, wo_due_date: {self.wo_due_date}, wo_link: {self.wo_link}"

    def __hash__(self):
        return self.wo_id.__hash__

    def __eq__(self, other):
        # print("__eq__ called")
        return str(self.wo_id) == str(other.wo_id)


def get_cbm():
    url = "https://portal.ez.na.rme.logistics.a2z.com/work-orders?organizationId=GYR1&customPreset=allOpen&preset=allOpen&type=CBM"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # need to do this once instance has started
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': CBM_PATH}}
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    driver.execute("send_command", params)
    driver.get(url)
    sleep(1)
    SignInASButton = driver.execute_script(
        "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('mwc-button:nth-child(4)').shadowRoot.querySelector('#button')")
    SignInASButton.click()
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
    sleep(15)

    CSVButton = driver.execute_script(
        "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
    CSVButton.click()
    sleep(10)


# engine = create_engine(
#     "sqlite:///C:/Users/deanejst/Documents/WEBHOOK/cbm/mydb.db", echo=True)
engine = create_engine(
    "sqlite:///C:/Users/netwokz/Documents/CODE/workspace/python/wo_database/mydb.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_cur_workorders() -> list[Workorder]:
    cur_wo_list = []
    df = pd.read_csv(CBM_FILE)
    for item in FINAL_EXCLUDED_COLUMNS:
        if item in df.columns:
            df = df.drop(columns=item)
    df = df.replace(np.nan, None)
    df = df.sort_values(by='Original PM due date', ascending=True)
    df.reset_index(inplace=True, drop=True)
    df_list = df.values.tolist()
    for item in df_list:
        print(item)
        work_oder = Workorder(item)
        cur_wo_list.append(work_oder)
        print(work_oder)
        print("\n")
    return cur_wo_list


def is_in_db(wo_id: str) -> bool:
    workorder = session.query(Workorder).get(wo_id)
    if workorder is None:
        return False
    return True


def not_in_db(wo_id: str) -> bool:
    workorder = session.query(Workorder).get(wo_id)
    if workorder is None:
        return True
    return False


def delete_entry(work_order: Workorder):
    # workorder = session.query(Workorder).get("87150830")
    session.delete(work_order)
    session.commit()


def add_entry(work_order: Workorder):
    session.add(work_order)
    session.commit()


def populate_db(workorders: list[str]):
    for item in workorders:
        work_oder = Workorder(item)
        if not_in_db(work_oder.get_id()):
            session.add(work_oder)
            session.commit()
        else:
            print(f"Workorder {work_oder.get_id()} already exists")


def get_all_entries() -> list[Workorder]:
    results = session.query(Workorder).all()
    return results


def get_wo_from_db(wo_id: str) -> Workorder:
    workorder = session.query(Workorder).get(wo_id)
    return workorder


def compare_db_entries():
    db_workorders = get_all_entries()
    cur_workorders = get_cur_workorders()

    if len(db_workorders) != 0:
        for workorder in db_workorders:
            if workorder not in cur_workorders:
                delete_entry(workorder)
                print(f"Workorder {workorder.get_id()} deleted successfully")
            else:
                print(f"Workorder {workorder.get_id()} kept")

    for workorder in cur_workorders:
        if workorder not in db_workorders:
            add_entry(workorder)
        else:
            print(f"Workorder {workorder.get_id()} already exists")


def get_df_values() -> pd.DataFrame:
    work_orders = get_all_entries()
    dict_list = []
    for wo in work_orders:
        # print(wo)
        dict_list.append(wo.get_df_data())
    wo_df = pd.DataFrame.from_dict(dict_list)
    return wo_df


def send_fail_notification():
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": WEBHOOK_FAILED_MSG})
    response = requests.post(MY_TEST_URL, headers=headers, data=data)
    # print(response.status_code)


def send_webhook(url, my_data):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({"data": my_data})
    response = requests.post(MY_TEST_URL, headers=headers, data=data)
    print(response.status_code)
    if response.status_code != 200:
        send_fail_notification()


def parse_csv():
    df = get_df_values()
    for item in FINAL_EXCLUDED_COLUMNS:
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
            # send_webhook(URL, tab)
            print(tab)
    print(f"Total number of WO's: {size}")


# if os.path.exists(CBM_FILE):
#     os.remove(CBM_FILE)
# get_cbm()
compare_db_entries()
parse_csv()
