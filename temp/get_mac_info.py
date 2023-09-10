import requests
import psutil

macs = ["18:e8:29:99:17:10", "b6:4b:f2:e6:f0:5f"]


def lookupMac(mac):
    for addr in [mac]:
        vendor = requests.get('http://api.macvendors.com/' + addr).text
        print(addr, vendor)


# Iterate over all the keys in the dictionary
for item in macs:
    print(item)
    lookupMac(item)
    break
