from random import randint

color_list = []

for i in range(100):
    color = '#%06X' % randint(0, 0xFFFFFF)
    if color not in color_list:
        color_list.append(color)

for color in color_list:
    print(color)
