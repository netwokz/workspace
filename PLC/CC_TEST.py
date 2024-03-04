from pylogix import PLC


def multi_ping(ip):
    with PLC(ip) as comm:
        tag = comm.Read("U160100_VFDParams.Source[18]")
        print(tag.TagName, tag.Value)


def get_stats():
    multi_ping("10.79.216.201")


get_stats()
