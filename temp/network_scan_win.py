import os
import re
full_results = [re.findall(
    '^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
final_results = [dict(zip(['IP', 'LAN_IP', 'MAC_ADDRESS'], i))
                 for i in full_results]
final_results = [{**i, **{'LAN_IP': i['LAN_IP'][1:-1]}} for i in final_results]
