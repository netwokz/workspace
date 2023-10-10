# Variable contains the path to the file
old_path = r"C:\Users\deanejst\Documents\CODE\workspace\smart-pac-tags.txt"
new_path = r"C:\Users\deanejst\Documents\CODE\workspace\smart-pac-tags-sorted.txt"

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

file_data = set([])

with open(old_path) as file:
    data = file.read()
    file_data.add(data)

for item in sorted(file_data):
    print(item)

with open(new_path, 'w+') as f:
     
    # write elements of list
    for items in sorted(file_data):
        f.write('%s\n' %items)
     