# FCLM master class for all FCLM needs.

import threading
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
        self._session = requests.Session()
        self._session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        self._session.verify = False
        self.fc = fc.upper()  # Making sure the FC is in uppercase
        self.pulls = []

    def get_rollup(self, rollup_type: str, span_type: str, start_date_time: pendulum.DateTime, end_date_time: pendulum.DateTime, **kwargs):
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
        url = f"https://fclm-portal.amazon.com/reports/{rollup_type}"
        params = {"warehouseId": self.fc, "spanType": span_type.title(), "reportFormat": "CSV"}  # <--- Change here

        # Dealing with kwargs
        for key in kwargs:
            params[key] = kwargs[key]

        # Dealing with span type
        if span_type.lower() == "month":  # <--- Change here
            params["startDateMonth"] = start_date_month
        elif span_type.lower() == "week":  # <--- Change here
            params["startDateWeek"] = start_date_week
        elif span_type.lower() == "day":  # <--- Change here
            params["startDateDay"] = start_date_day
        elif span_type.lower() == "intraday":  # <--- Change here
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
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False)
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
                    print(f"Failed to get {rollup_type} for {self.fc} {span_type} {start_date_time} {end_date_time}")
                    tries += 1
            except Exception as e:
                print(f"Failed to get {rollup_type} for {self.fc} {span_type} {start_date_time} {end_date_time}")
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

    def get_roster(self, params={}):
        url = "https://fclm-portal.amazon.com/employee/employeeRoster"
        default_params = {"warehouseId": self.fc, "reportFormat": "CSV", "submit": "true"}
        default_params.update(params)  # merge the additional params
        tries = 1
        while tries < 4:
            try:
                response = requests.get(url, params=default_params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False)
                if response.status_code == 200:
                    return pd.read_csv(StringIO(response.text))
                else:
                    print(response.status_code)
                    print(f"1 Failed to get roster for {self.fc}")
                    self.reset_mw_cookie()
                    tries += 1
            except Exception as e:
                print(f"2 Failed to get roster for {self.fc}")
                tries += 1
        return None

    def get_activity_details(
        self,
        employee_id: str,
        start_date: str,
        end_date: str,
        start_hour: str,
        end_hour: str,
        start_minute: str = "0",
        end_minute: str = "0",
        span_type: str = "Intraday",
        max_intraday_days: str = "1",
    ):
        url = "https://fclm-portal.amazon.com/employee/activityDetails"
        params = {
            "reportFormat": "CSV",
            "employeeId": employee_id,
            "warehouseId": self.fc,
            "startDateDay": start_date,
            "maxIntradayDays": max_intraday_days,
            "spanType": span_type,
            "startDateIntraday": start_date,
            "startHourIntraday": start_hour,
            "startMinuteIntraday": start_minute,
            "endDateIntraday": end_date,
            "endHourIntraday": end_hour,
            "endMinuteIntraday": end_minute,
        }

        # Print the parameters
        print(params)

        tries = 1
        while tries < 4:
            try:
                response = requests.get(url, params=params, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False)

                # Print the response status code
                print("Response status code:", response.status_code)

                if response.status_code == 200:
                    # Print the response text
                    print("Response text:", response.text)

                    return pd.read_csv(StringIO(response.text))
                else:
                    print(f"Failed to get activity details for employee ID {employee_id}")
                    tries += 1
            except Exception as e:
                print(f"Failed to get activity details for employee ID {employee_id}")
                tries += 1
        return None
