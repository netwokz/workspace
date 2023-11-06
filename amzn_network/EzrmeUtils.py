from time import sleep
from selenium import webdriver
import chromedriver_autoinstaller
import os


CSV_FILE = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\WorkOrderExport.csv"
CSV_PATH = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\"

USERNAME = "deanejst@amazon.com"
PASSWORD = "Emagdnim9#"

chromedriver_autoinstaller.install(cwd=True)


class DownloadUtils:
    def download_to_csv(url: str) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920,1080")
        prefs = {'download.default_directory': CSV_PATH}
        options.add_experimental_option('prefs', prefs)
        print("options added")
        driver = webdriver.Chrome(options=options)
        print("driver set to chrome")
        driver.get(url)
        print("Page LOADED")

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
        sleep(3)

        passwd = driver.execute_script(
            "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#password')")
        passwd.click()
        passwd.send_keys(PASSWORD)
        sleep(3)

        sign_on = driver.execute_script(
            "return document.querySelector('ez-rme-app').shadowRoot.querySelector('ez-login-page').shadowRoot.querySelector('ez-login').shadowRoot.querySelector('#submit-login')")
        sign_on.click()
        print("Sign On CLICKED")
        sleep(15)

        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        CSVButton = driver.execute_script(
            "return document.querySelector('body > ez-rme-app').shadowRoot.querySelector('#content > main > ez-work-order-list-page').shadowRoot.querySelector('div > mwc-button:nth-child(1)').shadowRoot.querySelector('#button')")
        CSVButton.click()
        print("CSV Downloaded")
        sleep(3)
