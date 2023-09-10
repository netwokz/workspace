MM_CONVERSION = 25.4
INCHES_LIST = [68,73,0,94,99,106,113,121,127,133,141]
MM_LIST = [1638,1811,1984,2156,2329,2502,2674,2847,3020,3192,3365,3538]

def inches_to_mm(measurment):
    conversion = measurment * MM_CONVERSION
    return int(conversion)

def mm_to_inches(measurment):
    conversion = measurment / MM_CONVERSION
    return int(conversion)

def get_difference(var1, var2):
    temp = var1 - var2
    return temp

converted_list = [1727, 1854, 0, 2387, 2514, 2692, 2870, 3073, 3225, 3378, 3581]
count = 0
for measurment in INCHES_LIST:
    # print(f"Belt {count}: {measurment} inches is {inches_to_mm(measurment):0.2f} mm")
    print(f"Belt {count+1} is {inches_to_mm(measurment)} mm, should be {MM_LIST[count]}. Difference of {get_difference(converted_list[count],MM_LIST[count])} mm or {mm_to_inches(get_difference(converted_list[count],MM_LIST[count]))} inches")
    # converted_list.append(int(inches_to_mm(measurment)))
    count += 1

# print(converted_list)