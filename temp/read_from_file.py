# Variable contains the path to the file
path = r"C:\Users\deanejst\Desktop\sk.dat"

# The file is read and its data is stored
# data = open(path, 'r').read()

# We splitted the string based on the
# occurrence of newline character
# A new list is created where newline
# character is not present in any element
# data_list = data.split("\n")

# Displaying the resultant data
# for data in data_list:
# print(data)


with open(path) as file:
    data = file.read()

print(data)
