from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

Base = declarative_base()
EXCLUDED_COLUMNS = ['Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority',
                    'Equipment Description', 'Status', 'Index']
CBM_PATH = os.path.expanduser("~\\Documents\\WEBHOOK\\cbm\\")
CBM_FILE = os.path.expanduser(
    "~\\Documents\\WEBHOOK\\cbm\\WorkOrderExport.csv")


class Workorder(Base):
    __tablename__ = 'workorders'

    wo_id = Column('Workorder ID', String, primary_key=True)
    wo_desc = Column('Description', String)
    wo_owner = Column('WO Owner', String)
    wo_due_date = Column('Original PM due date', String)
    wo_link = Column('Link', String)
    wo_type = Column('Type', String)
    wo_equip_crit = Column('Equipment Criticality', String)
    wo_equip_alias = Column('Equipment Alias', String)
    wo_equip = Column('Equipment', String)

    def __init__(self, wo_item):
        self.wo_id = wo_item[0]
        self.wo_desc = wo_item[1]
        self.wo_type = wo_item[2]
        self.wo_equip = wo_item[3]
        self.wo_equip_alias = wo_item[4]
        self.wo_equip_crit = wo_item[5]
        self.wo_owner = wo_item[6]
        self.wo_due_date = wo_item[7]
        self.wo_link = wo_item[8]

    def get_id(self):
        return self.wo_id

    def __repr__(self):
        return f"{self.wo_id} {self.wo_owner} {self.wo_equip} {self.wo_due_date} {self.wo_link}"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv(CBM_FILE)
for item in EXCLUDED_COLUMNS:
    if item in df.columns:
        df = df.drop(columns=item)
df = df.sort_values(by='Original PM due date', ascending=True)
df.reset_index(inplace=True, drop=True)
df_list = df.values.tolist()

# print(df_list[2])


def is_in_db(wo_id):
    workorder = session.query(Workorder).get(wo_id)
    if workorder is None:
        return False
    return True


def not_in_db(wo_id):
    workorder = session.query(Workorder).get(wo_id)
    if workorder is None:
        return True
    return False


def delete_entry(work_order):
    # workorder = session.query(Workorder).get("87150830")
    session.delete(work_order)
    session.commit()


def populate_db():
    for item in df_list:
        work_oder = Workorder(item)
        if not_in_db(work_oder.get_id()):
            session.add(work_oder)
            session.commit()
        else:
            print(f"Workorder {work_oder.get_id()} already exists")


def get_all_entries():
    results = session.query(Workorder).all()
    return results


def get_wo_from_db(wo_id):
    workorder = session.query(Workorder).get(wo_id)
    return workorder


def compare_db_entries():
    # Logic to get new WO's from CSV and compare against DB. Delete old out of DB, add new
    pass


populate_db()

# all_workorders = get_all_entries()
# for wo in all_workorders:
#     print(wo)
