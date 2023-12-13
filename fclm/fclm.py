# FCLM master class for all FCLM needs.

import os
import threading
import time
from enum import Enum
from io import StringIO

import pandas as pd
import pendulum
import requests
from requests_kerberos import OPTIONAL, HTTPKerberosAuth
from urllib3 import disable_warnings


# Creating enums for the ease of use
class SpanType(Enum):
    INTRADAY = "Intraday"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


class RollupType(Enum):
    FUNCTION_ROLLUP = "functionRollup"
    PROCESS_PATH_ROLLUP = "processPathRollup"
    TIME_ON_TASK = "timeOnTask"


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

    def get_rollup(self, rollup_type: RollupType, span_type: SpanType, start_date_time: pendulum.DateTime, end_date_time: pendulum.DateTime, **kwargs):
        """
        Gets the rollup for the specified inputs

        :param rollup_type: Rollup type (functionRollup, processPathRollup)
        :param span_type: span type (Intraday, Day, Week, Month)
        :param start_date_time: A DateTime object that denotes starting time
        :param end_date_time: A DateTime object that denotes ending time
        :param kwargs: Additional parameters for the rollup
        :return: A pandas DataFrame with the rollup data
        """

        # Setting the URL and parameters
        start_date_month = f"{start_date_time.format('YYYY-MM')}-01"
        start_date_week = start_date_time.add(days=1).subtract(days=start_date_time.weekday()).format("YYYY-MM-DD")
        start_date_day = start_date_time.format("YYYY-MM-DD")
        end_date_day = end_date_time.format("YYYY-MM-DD")

        tries = 1
        url = f"https://fclm-portal.amazon.com/reports/{rollup_type.value}"
        params = {"warehouseId": self.fc, "spanType": span_type.value.title(), "reportFormat": "CSV"}

        # Dealing with kwargs
        for key in kwargs:
            params[key] = kwargs[key]

        # Dealing with span type
        match span_type.value.lower():
            case "month":
                params["startDateMonth"] = start_date_month
            case "week":
                params["startDateWeek"] = start_date_week
            case "day":
                params["startDateDay"] = start_date_day
            case "intraday":
                params["startDateIntraday"] = start_date_day
                params["startHourIntraday"] = str(start_date_time.hour)
                params["startMinuteIntraday"] = str(max([y for y in [00, 15, 30, 45, start_date_time.minute] if y < start_date_time.minute + 1]))
                params["endDateIntraday"] = end_date_day
                params["endHourIntraday"] = str(end_date_time.hour)
                params["endMinuteIntraday"] = str(max([y for y in [00, 15, 30, 45, end_date_time.minute] if y < end_date_time.minute + 1]))
                params["maxIntradayDays1"] = 1
        while tries < 4:
            try:
                # Sending the request
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
                # Checking if the request was successful
                if response.status_code == 200:
                    # Converting the response to a pandas DataFrame
                    pull = {"fc": self.fc, "span_type": span_type, "start_date_time": start_date_time, "end_date_time": end_date_time, "dataframe": pd.read_csv(StringIO(response.text))}
                    for key in kwargs:
                        pull[key] = kwargs[key]
                    # Adding the pull to the pulls list for future reference
                    self.pulls.append(pull)
                    return pull["dataframe"]
                else:
                    print(f"Failed to get {rollup_type.value} for {self.fc} {span_type} {start_date_time} {end_date_time}")
                    self.reset_mw_cookie()
                    tries += 1
            except Exception as e:
                print(f"Failed to get {rollup_type.value} for {self.fc} {span_type} {start_date_time} {end_date_time}")
                tries += 1
        return None

    def get_function_rollups(self, process_ids: list, span_type: SpanType, start_date_time: pendulum.DateTime, end_date_time: pendulum.DateTime):
        """
        Gets the function rollups for the specified inputs by sending multiple requests in parallel

        :param process_ids: Process IDs for the rollup
        :param span_type: span type (Intraday, Day, Week, Month)
        :param start_date_time: A DateTime object that denotes starting time
        :param end_date_time: A DateTime object that denotes ending time
        :return: A pandas DataFrame with the rollup data
        """

        # Creating a list of threads
        threads = []
        global pulls
        pulls = list()

        # Sending multiple requests at once and then combining them into a single DataFrame
        for process_id in process_ids:
            threads.append(threading.Thread(target=self.get_rollup, args=(RollupType.FUNCTION_ROLLUP, span_type, start_date_time, end_date_time), kwargs={"processId": process_id}))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        results = None
        for result in pulls:
            if results is None:
                results = result[5]
            else:
                results = pd.concat([results, result[5]])
        return results

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
        Gets the roster for the specified FC

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

    def get_permissions(self, employee):
        """
        Gets the roster for the specified FC

        :return: A pandas DataFrame with the roster data
        """
        url = "https://fclm-portal.amazon.com/employee/search"
        params = {"term": employee, "warehouseId": self.fc}
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
                print(f"Exception! Failed to get roster for {self.fc}")
                tries += 1
        return None

    def get_activity_details(self, employee_id: str, start_datetime: pendulum.DateTime, end_datetime: pendulum.DateTime):
        """
        Gets the activity details of an employee by utilizing the activityDetails page

        :param employee_id: The employee ID of the employee
        :param start_datetime: The start datetime of the activity details
        :param end_datetime: The end datetime of the activity details
        :return: A pandas DataFrame with the activity details
        """

        # Formats used for start and end dates: 2022-11-24T00:00:00-0500
        url = "https://fclm-portal.amazon.com/employee/activityDetails"
        params = {
            "employeeId": employee_id,
            "warehouseId": self.fc,
            "startTime": start_datetime.format("YYYY-MM-DDTHH:mm:ssZZ"),
            "endTime": end_datetime.format("YYYY-MM-DDTHH:mm:ssZZ"),
            "reportFormat": "CSV",
            "submit": "true",
        }
        tries = 1
        while tries < 4:
            try:
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False, cookies=self.cookie)
                if response.status_code == 200:
                    print("Response: " + response.text)
                    return pd.read_csv(StringIO(response.text))
                else:
                    print(f"Failed to get activity details for {employee_id}")
                    self.reset_mw_cookie()
                    tries += 1
            except Exception as e:
                print(f"Failed to get activity details for {employee_id}")
                tries += 1
        return None


if __name__ == "__main__":
    fclm = FCLM("GYR1")
    roster = fclm.get_roster()
    print(roster.head())
