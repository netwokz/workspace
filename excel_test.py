import pandas as pd
import os
import pandas as pd
import xlrd

PATH = "C:\\Users\\deanejst\\Documents\\WEBHOOK\\"

wb = pd.read_excel(os.path.join(PATH, 'temp.xlsx'))
print(wb)
