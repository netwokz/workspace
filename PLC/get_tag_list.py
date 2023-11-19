from pylogix import PLC

tag_list = []

with PLC("10.79.216.253") as comm:
    tags = comm.GetTagList()
    for tag in tags.Value:
        tag_list.append(tag.TagName)

# for tag in tag_list:
#     print(tag)

tag_list.sort()

with open("temp_cabinet.txt", "w") as file1:
    # Writing data to a file
    # file1.write("Hello \n")
    for line in tag_list:
        file1.write(line + "\n")
