import json

PATH = "C:\\Users\\deanejst\\Documents\\CODE\\workspace\\temp\\"

# Opening JSON file
with open(PATH + 'IP_DICT.json') as json_file:
    global data
    data = json.load(json_file)

myKeys = list(data.keys())
myKeys.sort()
sorted_dict = {i: data[i] for i in myKeys}


def split_ip(ip):
    """Split a IP address given as string into a 4-tuple of integers."""
    return tuple(int(part) for part in ip.split('.'))


def my_key(item):
    return split_ip(item[0])


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


items = sorted(data.items(), key=my_key)

# print(data)
print(items)
print(Convert(items))
