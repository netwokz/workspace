sp_list = []
ip_list = []

for x in range(1,16):
    if x < 6:
        sp = f"SP 5-{x}"
        sp_list.append(sp)
    if x >= 6 and x < 11:
        sp = f"SP 6-{x}"
        sp_list.append(sp)
    if x >= 11:
        sp = f"SP 7-{x}"
        sp_list.append(sp)
        
for i in range(149,180):
    # print(f"10.18.8.{i}")
    ip_list.append(f"10.18.8.{i}")
    

with open("ips.txt", "w") as file1:
    # Writing data to a file
    for line in sp_list:
        data = f"\"{line}\" : \"\"" + '\n'
        file1.write(data)
    # for line in ip_list:
    #     file1.write(line + '\n')