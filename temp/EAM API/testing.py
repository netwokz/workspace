import requests
import json
import os

ssl_file = os.path.expanduser("~\\Desktop\\eam.amazon.com.pem")

api_call = "GRID_ID=93&GRID_NAME=WSJOBS&DATASPY_ID=887414&MADDON_FILTER_ALIAS_NAME_1=duedate&MADDON_FILTER_OPERATOR_1=%3C%3D&MADDON_FILTER_JOINER_1=AND&MADDON_FILTER_SEQNUM_1=1&MADDON_FILTER_VALUE_1=09%2F23%2F2023&MADDON_LPAREN_1=false&MADDON_RPAREN_1=false&USER_FUNCTION_NAME=WSJOBS&SYSTEM_FUNCTION_NAME=WSJOBS&CURRENT_TAB_NAME=LST&COMPONENT_INFO_TYPE=DATA_ONLY&eamid=20ea1ddc-7246-4464-829d-51bf00a63961&tenant=PROD"

api_url = "https://eam.amazon.com/web/base/WSJOBS.xmlhttp?"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# new_data = requests.post(api_url, headers=headers, data=api_call)
new_data = requests.get("https://eam.amazon.com/web/base/WSJOBS.xmlhttp?GRID_ID=93&GRID_NAME=WSJOBS&DATASPY_ID=887414&MADDON_FILTER_ALIAS_NAME_1=duedate&MADDON_FILTER_OPERATOR_1=%3C%3D&MADDON_FILTER_JOINER_1=AND&MADDON_FILTER_SEQNUM_1=1&MADDON_FILTER_VALUE_1=09%2F23%2F2023&MADDON_LPAREN_1=false&MADDON_RPAREN_1=false&USER_FUNCTION_NAME=WSJOBS&SYSTEM_FUNCTION_NAME=WSJOBS&CURRENT_TAB_NAME=LST&COMPONENT_INFO_TYPE=DATA_ONLY&eamid=20ea1ddc-7246-4464-829d-51bf00a63961&tenant=PROD", headers=headers, verify=ssl_file)

print(new_data)
# print(ssl_file)
