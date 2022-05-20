from pickle import FALSE
import platform
import subprocess
import os

server_online = FALSE
plat = platform.system()


def ping(host):
    global server_online
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]  
    try:
        subprocess.call(command)
        server_online = True
    except Exception:
        server_online = False


def ask_user():
    host = input('What\'s the host to try? ')
    ping(host)


host = '10.10.10.10'

print("---- Trying to Ping a Server with IPAddress ----  " + host)

# Check for Windows and Linux Platforms
if plat == "Windows":
    response = os.system("ping -n 1 " + host)
    pass

elif plat == "Linux":
    response = os.system("ping -c 1 -W 3 " + host)
    pass

# Check for response status code
if response == 0:
    print("********************************************************************")
    print(host, 'is UP and reachable!')
    print("********************************************************************")
    print("\n")
elif response == 2 or 256 or 512:
    print("********************************************************************")
    print(host, 'is DOWN and No response from Server!')
    print("********************************************************************")
    print("\n")
else:
    print("********************************************************************")
    print(host, 'is DOWN and Host Unreachable!')
    print("********************************************************************")
    print("\n")


# ask_user()

# ping('googlse.com')
#print('Server is Online ' if server_online == True else 'Server is Offline ' )
