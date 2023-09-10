import sys
import telnetlib
from ftplib import FTP
import time
import cv2

# cognex's config
ip = "10.79.218.142"
user = 'admin'
password = ''

# telnet login
tn = telnetlib.Telnet(ip)
telnet_user = user+'\r\n'
tn.write(telnet_user.encode('ascii'))  # the user name is admin
# there is no password - just return - now logged in
tn.write("\r\n".encode('ascii'))
# print('Telnet Logged in')

# capture
tn.write(b"SE8\r\n")

# ftp login
ftp = FTP(ip)
ftp.login(user)
# print('FTP logged in')

# show all file in cognex
# files_list = ftp.dir()
# print(files_list)

# download file from cognex
filename = 'image.bmp'
lf = open(filename, "wb")
ftp.retrbinary("RETR " + filename, lf.write)
lf.close()

image = cv2.imread('image.bmp')
cv2.imshow('Image', image)

cv2.waitKey(0)
