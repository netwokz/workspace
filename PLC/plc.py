from pylogix import PLC
from time import sleep
import asyncio
import time

tag_list = []

sp_dict = {
    "SP 5-1" : "10.18.8.137",
    "SP 5-2" : "10.18.8.140",
    "SP 5-3" : "10.18.8.143",
    "SP 5-4" : "10.18.8.146",
    "SP 5-5" : "10.18.8.149",
    "SP 6-6" : "10.18.8.152",
    "SP 6-7" : "10.18.8.155",
    "SP 6-8" : "10.18.8.158",
    "SP 6-9" : "10.18.8.161",
    "SP 6-10" : "10.18.8.164",
    "SP 7-11" : "10.18.8.167",
    "SP 7-12" : "10.18.8.170",
    "SP 7-13" : "10.18.8.173",
    "SP 7-14" : "10.18.8.176",
    "SP 7-15" : "10.18.8.179"
}

async def test():
    print('Hello world!')
    await asyncio.sleep(1)
    print('Hello again!')

def ping_sp(sp, ip):
        with PLC(ip) as comm:
            op_auto = comm.Read("Operational_Mode_Auto_Active")
            if op_auto.Value == True:
                print(f"{sp} is online")  
            else:
                print(f"{sp} is offline")


print(f"Started: {time.strftime('%X')}")
for sp, ip in sp_dict.items():
    # asyncio.run(ping_sp(sp, ip))
    ping_sp(sp, ip)

print(f"Finished: {time.strftime('%X')}")

# with PLC("10.79.219.62") as comm:
#     op_auto = comm.Read("AutoMode")
#     # for t in tags.Value:
#     #     print("Tag:", t.TagName, t.DataType)
#     # print("Tag:", tags.TagName, tags.Status, tags.Value)
#     print(f"Operational_Mode_Auto_Active is {op_auto.Value}")