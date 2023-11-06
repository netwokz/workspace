from pylogix import PLC
import sqlite3
import os

CURRENT_DIR = os.getcwd()
DB_NAME = "plc_data.db"

def get_user_folder():
    if os.name == "nt":
        return f"{os.getenv('USERPROFILE')}\\"
    else:  # PORT: For *Nix systems
        return f"{os.getenv('HOME')}/"

db = sqlite3.connect(os.path.join(get_user_folder(), DB_NAME))
cursor = db.cursor()

cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='plc' ''')
#if the count is 1, then table exists
if cursor.fetchone()[0]==1 : 
	# Table exists
    pass
else :
	# Table does not exist.
    cursor.execute("CREATE TABLE plc (name TEXT, entry TEXT, time TEXT)")

get_user_folder()

for x in range(1,16):
    cursor.execute(f"INSERT INTO plc VALUES ('SP7-{x}', 'manual', '2023-5-08')")

# with PLC("10.18.8.176") as comm:
    # ret = comm.Read("Operational_Mode_Auto_Active")
    # print(ret.TagName, ret.Value, ret.Status)
    
rows = cursor.execute("SELECT name, entry, time FROM plc").fetchall()
for item in rows:
    print(item)