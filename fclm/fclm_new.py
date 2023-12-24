# FCLM master class for all FCLM needs.

import os
import time
from io import StringIO

import pandas as pd
import requests
from requests_kerberos import OPTIONAL, HTTPKerberosAuth
from urllib3 import disable_warnings


class FCLM:
    def __init__(self, fc: str):
        """
        Initializes the FCLM class
        :param fc: The FC to be used
        """
        disable_warnings()  # Disabling warnings for SSL
        self.fc = fc.upper()  # Making sure the FC is in uppercase
        self.pulls = []
        self.cookie = self.mw_cookie()

        # Sending a request to the FCLM portal to make sure the cookie is valid
        try:
            response = requests.get("https://fclm-portal.amazon.com", auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
            if response.status_code != 200:
                self.reset_mw_cookie()
                response = requests.get("https://fclm-portal.amazon.com", auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
            print("Authenticated to FCLM portal")
        except Exception as e:
            print("Failed to authenticate to FCLM portal")

    def reset_mw_cookie(self, flags: list = None):
        """
        Resets the cookie for the FCLM portal
        :param flags: Flags to be used for mwinit
        :return: None
        """
        self.cookie = self.mw_cookie(flags=flags, delete_cookie=True)

    def mw_cookie(self, flags=None, delete_cookie: bool = False):
        """
        Checks if the cookie file exists in the .midway folder in the userprofile location.
        It then validates the cookie making sure it is not expired.
        It uses OTP authentication to make the cookie reusable for 20 hrs.

        :return: A cookie list that can used with a requests.Session()
        """
        # Setting defaults for midway cookie location
        if flags is None:
            flags = ["-o", "--aea"]
        path = os.path.join(os.path.expanduser("~"), ".midway")
        cookie = os.path.join(path, "cookie")

        if delete_cookie:
            os.remove(cookie)

        if not os.path.exists(cookie):
            os.system(f"mwinit {' '.join(flags)}")

        with open(cookie, "rt") as c:
            cookie_file = c.readlines()

        cookies = {}
        # Opening the file and looking at timestamp for expired cookie, running mwinit -o again or getting the cookie
        now = time.time()
        for line in range(4, len(cookie_file)):
            if int(cookie_file[line].split("\t")[4]) < now:
                os.system(f"mwinit {' '.join(flags)}")
                return self.mw_cookie(flags=flags)
            cookies[cookie_file[line].split("\t")[5]] = str.replace(cookie_file[line].split("\t")[6], "\n", "")
        return cookies

    def get_roster(self):
        """
        Gets the roster for the specified FC

        :return: A pandas DataFrame with the roster data
        """
        url = "https://fclm-portal.amazon.com/employee/employeeRoster"
        params = {
            "warehouseId": self.fc,
            "reportFormat": "CSV",
            "submit": "true",
        }
        tries = 1
        while tries < 4:
            try:
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
                if response.status_code == 200:
                    return pd.read_csv(StringIO(response.text))
                else:
                    print(f"Failed to get roster for {self.fc}")
                    self.reset_mw_cookie()
                    tries += 1
            except Exception as e:
                print(f"Failed to get roster for {self.fc}")
                tries += 1
        return None

    def get_employees(self, supervisor):
        """
        Gets the roster for the specified Manager

        :return: A pandas DataFrame with the roster data
        """
        url = "https://fclm-portal.amazon.com/employee/employeeRoster"
        params = {"warehouseId": self.fc, "reportFormat": "CSV", "submit": "true", "supervisorLogin": supervisor}
        tries = 1
        while tries < 4:
            try:
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
                if response.status_code == 200:
                    return pd.read_csv(StringIO(response.text))
                else:
                    print(f"Failed to get roster for {self.fc}")
                    self.reset_mw_cookie()
                    tries += 1
            except Exception as e:
                print(f"Failed to get roster for {self.fc}")
                tries += 1
        return None


if __name__ == "__main__":
    fclm = FCLM("GYR1")
    roster = fclm.get_roster()
    print(roster.head())
