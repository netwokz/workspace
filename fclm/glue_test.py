import time
from functools import reduce

import pandas as pd
from fclm import *
from tabulate import tabulate

fclm = FCLM("GYR1")
EXCLUDED_COLUMNS = ["Badge Barcode ID", "Employment Type", "Employee Status", "Temp Agency Code", "Badge RFID", "Exempt", "Date2", "Management Area ID"]
MANAGERS = ["huntidan", "jneaus", "zdharr", "gavmcm", "salasjud", "mbrney", "cmayn", "stromgs", "kgresh"]

all_employees = []
dept_ids = ["1712", "1711"]


def parse_employee_csv():
    func1_st = time.time()
    # result = pd.read_csv("HSE1_roster_cleaned.csv")
    result = fclm.get_roster()
    result.to_csv("GYR1_roster.csv", index=False)
    rslt_df = result.loc[result["Department ID"].isin(dept_ids)]
    for item in EXCLUDED_COLUMNS:
        if item in rslt_df.columns:
            rslt_df = rslt_df.drop(columns=item)
    rslt_df = rslt_df.sort_values(by="Employee ID", ascending=True)
    rslt_df.reset_index(inplace=True, drop=True)
    final_rslt = tabulate(rslt_df, tablefmt="pipe", headers="keys", showindex=False)
    print(final_rslt)
    print(f"Total Techs: {len(rslt_df)}")
    rslt_df.to_csv("GYR1_parse_csv.csv", index=False)
    func1_et = time.time()
    elapsed_time = func1_et - func1_st
    print(f"parse_employee_csv() Execution time: {elapsed_time} seconds")


def get_employees():
    func2_st = time.time()
    all_dfs = []
    for manager in MANAGERS:
        all_dfs.append(fclm.get_employees(manager))
    rslt_df = pd.concat(all_dfs, axis=0)
    # rslt_df = df.loc[df["Department ID"].isin(dept_ids)]
    for item in EXCLUDED_COLUMNS:
        if item in rslt_df.columns:
            rslt_df = rslt_df.drop(columns=item)
    rslt_df = rslt_df.sort_values(by="Employee ID", ascending=True)
    rslt_df.reset_index(inplace=True, drop=True)
    final_rslt = tabulate(rslt_df, tablefmt="pipe", headers="keys", showindex=False)
    print(final_rslt)
    print(f"Total Techs: {len(rslt_df)}")
    rslt_df.to_csv("GYR1_get_employees.csv", index=False)
    func2_et = time.time()
    elapsed_time = func2_et - func2_st
    print(f"get_employees() Execution time: {elapsed_time} seconds")


# parse_employee_csv()
result = fclm.get_roster()
print(len(result))
