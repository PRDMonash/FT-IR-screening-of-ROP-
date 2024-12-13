from array import * 
import numpy as np
import os
import pandas as pd
import csv

def index_2d(myList, conversion):
    """
    this function is used to find the position of conversion in two array myList

    i is the index of intial concentration 
    np.where(x == conversion) is the index of residence time 
    """

    for i, x in enumerate(myList):
        if conversion in x:
            j_1 = np.where(x == conversion)
            j = j_1[0]
            return i, j



path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\5s-step\3D surface data\110Zdata.txt"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\5s-step\3D surface data"
filename =  os.path.splitext(os.path.split(path)[1])[0]
rawdata = np.loadtxt(path) 

print(rawdata.shape[0])
print(rawdata.shape[1])

Concentration = float(input("Please input the initial concentration (M):"))
index = int((Concentration - 0.5)/0.05)
Conversion = []
residencetime = []

for i in range(109):
    time = (60 + i*5)/60
    residencetime.append(time)

Con = []

for item in rawdata:
    con = item[index]
    Con.append(con)


# save converison vaeries from time data to csv file
with open(r'{}\{}-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'Residence time/minute':residencetime,
        'Conversion/%':Con,
}
        
column_names = ['Residence time/minute','Conversion/%']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-Data.csv'.format(path_t,filename), columns = column_names)        