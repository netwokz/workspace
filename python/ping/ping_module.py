from fileinput import filename
import platform
import subprocess

server_list = ["10.10.10.10"]

# filename = 'ip_list.txt'
# with open(filename, 'r') as reader:
#     content = reader.read();
#     server_list = content.split('\n')


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '2', host]
    try:
        response = subprocess.call(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception:
        print('Something went wrong!')
    if response == 0:
        print(f'{host} is Online')
    else:
        print(f'{host} is Offline')


for ip in server_list:
    ping(ip)
