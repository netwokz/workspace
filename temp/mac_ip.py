with open("MAC_ADDRS", "r") as filestream:
    for line in filestream:
        currentline = line.split(",")
        mac = currentline[0]
        ip = currentline[1].strip()
        print(f"{ip} has a MAC of {mac}")
