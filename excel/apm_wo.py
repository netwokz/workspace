# import pandas lib as pd
import csv
import os.path

import pandas as pd
from tabulate import tabulate

all_columns = [
    "Organization",
    "Priority Icon",
    "Work Order",
    "Description",
    "Status",
    "Type",
    "Hold Reason",
    "Department",
    "Equipment",
    "Equipment Description",
    "Assigned To",
    "Shift",
    "Assigned to Contractor",
    "Contractor Desc.",
    "Sched. Start Date",
    "Original PM Due Date",
    "Sched. End Date",
    "Total Booked Labor",
    "Parts Issued?",
    "Safety related",
    "SIM-T No.",
    "Date Created",
    "WO Execution",
]

excluded_columns = [
    "Organization",
    "Priority Icon",
    "Status",
    "Type",
    "Hold Reason",
    "Department",
    "Assigned to Contractor",
    "Contractor Desc.",
    "Sched. Start Date",
    "Total Booked Labor",
    "Parts Issued?",
    "Safety related",
    "SIM-T No.",
    "Date Created",
    "WO Execution",
]

shift_codes = {"YR19", "YR1Q", "YR1R", "YR1T", "None"}
# excluded_equipment = {"G.UTIL.WS.285", "AFE3.5.1.TOTE.06", "FIRE.SUP.SPRK", "SS.SRT.01.RCRC", "EXTEND.FLEXI.160425", "BOT.HDU.H1-NR-2029-526347", "EXTEND.FLEXI.160625", "HVAC", "AR"}
excluded_descriptions = {
    "AMER-MAXX REACH 3-25/80-30 13 WEEK PM",
    "CONDITION BASED MAINTENANCE STROBE CHECK FOR BELT 01W",
    "System Check - MHE",
    "AMER-DEMATIC MODEL 9570 3 MONTH PM SCHEDULE",
    "AMER - CONDITION BASED MAINTENANCE ULTRASOUND BEARING INSPECTION 13W",
    "AMER-NIKE 2.0 MULTIPURPOSE STATION ( AMAZON ROBOTICS 700-0012) 13 WEEK PM",
    "[GYR1-paKivaA01] - 1355 - Station Issues > Equipment problem at station",
    "AUTOSLAM 3.0 2ND DAILY INSPECTION",
    "AMER-DIRECTED PALLETIZATION SYSTEM - 13 WEEK",
    "AMER-DEMATIC 2430 - SL2 DAILY CHECK",
    "AMER-DEMATIC 8120 CONVEYOR 13 WEEK PM",
    "AMER-BBM - WEEKLY INTERIOR SYSTEM CHECK",
    "MCM[GYR1] CC652 Project",
    "AMER-FLS Monthly Inspection - Portable Fire Extinguishers",
    "AMER-GENERATOR RUN MONTHLY PM",
    "AMER-DEMATIC MODEL 8300 13 WEEK PM (NEW)",
    "AMER-TRANSNORM TS1500-140 V2-090 4 WEEK",
    "12 WEEKLY DEMATIC MAJOR PM SC3 CARRIER",
    "AMER-Amazon Control Cabinet 13Wk PM",
    "AMER-HIGH SPEED RAT 13 WEEK",
    "V-Belt replacement",
    "AMER-ATS SMARTPAC 3.2 DAILY",
    "AMER-ARSAW 4 Week PM",
    "AMER-ATS SMARTPAC 3.2 04 YEAR",
    "WEEKLY GAS DETECTORS INSPECTION",
    "AMER-ARB S7000 INTRALOX SORTER 13 WEEK PM",
    "AMER-INTRALOX DARB S4500 26 WEEK",
    "AMER-WEEKLY WORK CELL PM",
    "WEEKLY SPRINKLER SYSTEM AND PUMP CHECK",
    "AMER-CTM 360A PRINT APPLY MACHINE 13 WEEK PM",
    "INTRALOX DARB S4500 DAILY (AMERICAS)",
    "WEEKLY SPRINKLERS INSPECTION",
    "WEEKLY STERTIL DOCK DOOR COMBILOCK",
    "AMER-INTRALOX DARB S4500 DAILY",
    "AMER-GENERATOR INSPECTION 1 WK",
    "AMER-RESTROOM INSPECTION  (FRONT HALF)",
    "WEEKLY MHE RESPONDING TO CALLS",
    "AMER-H DRIVE BOTS 52 WEEK PM",
    "AMER-RESTROOM INSPECTION  (BACK HALF)",
    "AMER-SLAM DAILY SYSTEM CHECK",
    "AMER-DEMATIC MODEL 9190 13 WEEK  PM",
    "AMER-INTERROLL BW40 13 WEEK",
    "AMER-ATS SMARTPAC 3.2 13 WEEK",
    "AMER-SLAM WEEKLY",
    "AMER-AR FLOOR WITH PALLET POD SEGMENT 8 WEEK",
    "AMER-AR DELTA CHARGER 3.1(H&P) 26 WEEK PM",
    "AMER-ARSAW (DEMATIC 700-0012-176-NA) 13 WEEK",
    "AMER-AR FLOOR WITH HIGH TRAFFIC SEGMENT 4 WEEK",
    "AMER-AMAZON ROBOTICS PSC 700-0101-002-NA 26 WEEK",
    "AMER-Amazon Control Cabinet 26Wk PM",
    "AMER-FLS Weekly Testing and Inspection - Fire Pump, Electric & Diesel, No-Flow",
    "AMER-ARB S7000 INTRALOX SORTER 26 WEEK PM",
    "CONDITION BASED MAINTENANCE THERMOGRAPHIC INSPECTION FOR CONVEYOR 04W",
    "AMER-BBM - WEEKLY COMPACTOR/TRUCKYARD INSPECTION",
    "AMER-AR FLOOR WITH INVENTORY POD SEGMENT 12 WEEK",
    "AMER-ATS SMARTPAC 3.2 52 WEEK",
    "AMER-DEMATIC MODEL 8320 13 WEEK PM (NEW)",
    "AMER-DEMATIC 8130 O-RING DRIVEN ROLLER CONVEYOR 13 WEEK",
    "AMER-TRANSNORM TS1500-140 V2-180 4 WEEK",
    "Weekly Cleaning Dematic 2430",
    "BMS Alarm - Warehouse RTU Fan Failure Alarms",
    "AMER-BBM - WEEKLY DOCK FAN INSP / CLEAN",
    "AMER-ATS SMARTPAC 3.2 WEEKLY",
    "AMER-AMAZON BUILDING MANAGEMENT SYSTEM",
    "AMER-DEMATIC MODEL 9405 13 WEEK  PM",
    "AMER-Amazon Control Cabinet 52Wk PM",
    "AMER-AMBAFLEX SV MODEL SPIRAL 4 WEEK",
    "AMER-TRANSNORM TS1500-140 V2-030 4 WEEK",
    "AMER-ATS SMARTPAC 3.2 4WK",
    "AMER-MARATHON AST-440 4 WEEK PM",
}
needed_columns = {"REMEDY.FACILITIES"}

df = pd.read_excel("Sheet1.xlsx")
# for column in df.columns:
#     if column == "":
#     print(column)

for item in excluded_columns:
    if item in df:
        df = df.drop(columns=item)

df["Shift"] = df["Shift"].fillna("None")
# df["Original PM Due Date"] = df["Original PM Due Date"].fillna("None")
df["Sched. End Date"] = df["Sched. End Date"].fillna("None")
df = df.loc[df["Original PM Due Date"].notnull()]
df = df.loc[df["Shift"].isin(shift_codes)]
df = df.loc[~df["Description"].isin(excluded_descriptions)]
df = df.loc[~df["Description"].str.contains("FLEX")]
df = df.loc[~df["Description"].str.contains("GYR1-paKivaA01")]
df = df.loc[~df["Description"].str.contains("GYR1-paKivaA02")]
df = df.loc[~df["Description"].str.contains("GYR1-paKivaA03")]
df = df.loc[~df["Description"].str.contains("GYR1-paKivaA04")]
df = df.loc[~df["Equipment Description"].str.contains("EXTEND")]
df = df.loc[~df["Equipment"].str.contains("BOT.HDU")]
df = df.loc[~df["Equipment"].str.contains("AR.ZONE")]

df.reset_index(drop=True, inplace=True)
list_set = set()
data = []
# loop through the rows using iterrows()
for index, row in df.iterrows():
    if row[all_columns[8]] not in excluded_descriptions and row[all_columns[3]] not in excluded_descriptions:
        if row[all_columns[8]].startswith("EXTEND") or row[all_columns[8]].startswith("BOT") or row[all_columns[3]].startswith("[GYR1-paKivaA") or row[all_columns[8]].startswith("AR"):
            continue
        if row[all_columns[11]] not in shift_codes:
            continue
        data.append([row["Work Order"], row["Equipment"], row["Description"], row["Shift"]])
        list_set.add(row["Description"])

size = len(df.index)

# if size > 0:
#     dataframe_chunk_size = 30
#     list_df = [df[i : i + dataframe_chunk_size] for i in range(0, len(df), dataframe_chunk_size)]
#     for dataframe in list_df:
#         tab = tabulate(dataframe, tablefmt="pipe", headers="keys", showindex=False)
#         print(tab)

# file_name = "apm.csv"
# if os.path.isfile(file_name):
#     os.remove(file_name)

# with open("apm.csv", "w", newline="") as csvfile:
#     # creating a csv dict writer object
#     writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
#     # writing data rows
#     writer.writerows(data)

# for item in list_set:
#     print(f'"{item}",')
df.to_csv("df.csv")
# print(df)
