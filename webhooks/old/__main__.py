from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
import pandas as pd
import requests
from tabulate import tabulate
import json
import re
import chromedriver_autoinstaller

import argparse

WH_ID = "GYR1"
SLACK_API = "https://hooks.slack.com/workflows/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"

chromedriver_autoinstaller.install(cwd=True)

# parser = argparse.ArgumentParser(
#     description='SmartPac Webhook. Contact @byrcharl')
# parser.add_argument("WebhookLink", help="Slack Webhook link.")
# parser.add_argument("WHID", help="Warehouse ID.")
# args = parser.parse_args()


def METRICS():
    link = "https://grafana-prod.prod.us-east-1.grafana.insights.aft.amazon.dev/d/23b3a69d/smartpac?orgId=1&var-building=GYR1&var-workCellId=All&var-process=SmartPac&from=now-9h&to=now"
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    # sleep(10)

    all_avg = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="panel-4"]/div/div[1]/div/div[2]/div/plugin-component/panel-plugin-graph/grafana-panel/ng-transclude/div/div[2]/div/div[1]/div')))

    print(all_avg)

    lst = []
    for avg in all_avg:
        # print(avg.text)
        lst.append(avg.text)
    # print(lst)
    list = [x.replace('\n', ',')for x in lst]

    list_1 = ['SmartPac']
    list_2 = ['Availability']
    for string in list:
        temp = re.compile("(,|^)((\d+)(\.\d+)?)(,|$)").findall(string)
        list_1 += [x[1] for x in temp]
        temp = re.compile("(,|^)((\d+)(\.\d+)?%)(,|$)").findall(string)
        list_2 += [x[1] for x in temp]

    return list_1, list_2


def DateFrame():
    df = pd.DataFrame([list_2])

    df = (tabulate(df, headers=list_1, tablefmt="pipe",
          showindex=False, numalign="center",))
    print(df)
    return df


def WEBHOOK():
    # web_hook_link = args.WebhookLink
    web_hook_link = SLACK_API
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "wo_id": df,
    })

    response = requests.post(web_hook_link, headers=headers, data=data)
    print(response)


list_1, list_2 = METRICS()
df = DateFrame()
WEBHOOK()
