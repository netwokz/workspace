import sys

from pycomm3 import CIPDriver, LogixDriver, Services

ip = input("input IP Address: ")

IP = LogixDriver(ip)
drivepath = "10.166.77.6/bp/1/enet/11.200.1.9"

try:
    IP.open()
    plc_name = IP.get_plc_name()
    print(plc_name)
except:
    print("could not connect to " + ip)

try:
    with CIPDriver(drivepath) as drive:
        param = drive.generic_message(
            service=Services.get_attribute_single,
            class_code=b"\x93",
            instance=19,  # Parameter 19 = elapsed run time
            attribute=b"\x09",
            # data_type=int.from_bytes(),
            connected=False,
            unconnected_send=True,
            route_path=True,
            name="pf525_param",
        )
        result = int.from_bytes(param.value, byteorder=sys.byteorder)
        print(result)
except:
    print("drive stuff didnt work")
