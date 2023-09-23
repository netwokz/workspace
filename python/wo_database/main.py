from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()
EXCLUDED_COLUMNS = ['Organization', 'Precision WO', 'Created By', 'Shift ID', 'PM Compliance Max Date', 'PM Compliance Min Date', 'Scheduled Start Date', 'Scheduled End Date', 'Completed date', 'Priority',
                    'Equipment Description', 'Status', 'Index']


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

    # def __init__(self, wo_id, wo_desc, wo_type, wo_equip, wo_equip_alias, wo_equip_crit, wo_owner, wo_due_date, wo_link):
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


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv('WorkOrderExport.csv')
for item in EXCLUDED_COLUMNS:
    if item in df.columns:
        df = df.drop(columns=item)
df = df.sort_values(by='Original PM due date', ascending=True)
df.reset_index(inplace=True, drop=True)
df_list = df.values.tolist()

# print(df_list[2])
for item in df_list:
    work_oder = Workorder(item)
    session.add(work_oder)
session.commit()
