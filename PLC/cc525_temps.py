from pylogix import PLC

tags_list = [
    # "DPASI_01_TS.MAX_TEMP",
    "DPASI_01_TS.CURR_TEMP",
    "DPASI_02_TS.CURR_TEMP",
    "DPASI_03_TS.CURR_TEMP",
    "DPASI_04_TS.CURR_TEMP",
    "DPASI_05_TS.CURR_TEMP",
    "DPASI_06_TS.CURR_TEMP",
    "DPASI_07_TS.CURR_TEMP",
    "IS11_TS.CURR_TEMP",
    "IS12_TS.CURR_TEMP",
    "IS13_TS.CURR_TEMP",
    "IS14_TS.CURR_TEMP",
    "IS15_TS.CURR_TEMP",
    "IS16_TS.CURR_TEMP",
    "IS21_TS.CURR_TEMP",
    "IS22_TS.CURR_TEMP",
    "IS23_TS.CURR_TEMP",
    "IS24_TS.CURR_TEMP",
    "IS25_TS.CURR_TEMP",
    "IS26_TS.CURR_TEMP",
    "LSMC_01_TS.CURR_TEMP",
    "LSMC_02_TS.CURR_TEMP",
    "LSMC_03_TS.CURR_TEMP",
    "LSMC_04_TS.CURR_TEMP",
    "LSMC_05_TS.CURR_TEMP",
    "LSMC_06_TS.CURR_TEMP",
    "LSMC_07_TS.CURR_TEMP",
    "LSMC_08_TS.CURR_TEMP",
    "LSMC_09_TS.CURR_TEMP",
    "LSMC_10_TS.CURR_TEMP",
    "LSMC_11_TS.CURR_TEMP",
    "MSC1_TS.CURR_TEMP",
    "MSC2_TS.CURR_TEMP",
    "POINT_IO_01_TS.CURR_TEMP",
    "POINT_IO_02_TS.CURR_TEMP",
    "POINT_IO_03_TS.CURR_TEMP",
    "POINT_IO_04_TS.CURR_TEMP",
]

temps = {}


def get_temps():
    with PLC("10.79.217.250") as comm:
        nc_ret = comm.Read(tags_list)
        for tag in nc_ret:
            print(f"{tag.TagName}: {tag.Value:.0f}°")
            # send_notification("E-Stop!", f"E-Stop condition at {parse_name(tag.TagName)}")


get_temps()

for temp in temps:
    print(f"{temp}: {temps[temp]}")
