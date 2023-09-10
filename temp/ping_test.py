from fileinput import filename
from http import server
import platform
import subprocess
import webbrowser

server_list = []

servers = "192.168.43."

# filename = 'ip.txt'
# with open(filename, 'r') as reader:
#    content = reader.read();
#    server_list = content.split('\n')


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        response = subprocess.call(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception:
        print('Something went wrong!')
        return False
    if response == 0:
        print('{} is Online'.format(host))
        print(response)
        return True
    else:
        # print('{} is Offline'.format(host))
        return False


def do_pings():
    for x in range(100, 200):
        server = servers + str(x)
        print(f"Trying {server}")
        ping(server)


# def open_website():
#     for x in range(220,240):
#         url = "http://10.79.221." + str(x) + "/remote.html"
#         webbrowser.open(url)

# open_website()

do_pings()
