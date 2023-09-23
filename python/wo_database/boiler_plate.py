# import db_helper as db
from db_helper import WODBHelper as db
import csv
import json
from tabulate import tabulate
import pandas as pd

# db.init_db()

# db.add_entry()

# Function to convert a CSV to JSON
# Takes the file paths as arguments


def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        data['data'] = []

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # set 'data' as the primary key
            data['data'].append(rows)

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


csvFilePath = r'WorkOrderExport.csv'
jsonFilePath = r'data.json'

# Call the make_json function
# make_json(csvFilePath, jsonFilePath)

# with open("data.json", "r") as read_file:
#     data = json.loads(read_file.read())

# for item in data['data']:
#     print(item[4])

# wo_id TEXT, desc TEXT, type TEXT, owner TEXT, max TEXT, link TEXT

# print(data['data'])
# print(tabulate(data, headers="keys"))

EXCLUDED_COLUMNS = ['Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority',
                    'Equipment Description', 'Status', 'Index']

ALL_COLUMNS = ['Type', 'Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority', 'Equipment Criticality',
               'Equipment Alias', 'Equipment Description', 'Status', 'Equipment', 'Index', 'Workorder ID', 'Description', 'WO Owner', 'Original PM due date', 'Link']
df = pd.read_csv(csvFilePath)
for item in EXCLUDED_COLUMNS:
    if item in df.columns:
        df = df.drop(columns=item)
df = df.sort_values(by='Original PM due date', ascending=True)
df.reset_index(inplace=True, drop=True)
tab = tabulate(df, tablefmt="pipe",
               headers="keys", showindex=False)
# print(tab)

df_list = df.values.tolist()
for item in df_list:
    # [wo_id, wo_desc, wo_type, wo_equip,wo_equip_alias,wo_equip_crit,wo_owner, wo_due_date, wo_link]
    print(item)
