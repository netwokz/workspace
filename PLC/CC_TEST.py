import customtkinter
from pylogix import PLC


def multi_ping(ip):
    with PLC(ip) as comm:
        speed = comm.Read("XB1")
        print(speed)


def get_stats():
    multi_ping("10.79.216.223")


get_stats()
