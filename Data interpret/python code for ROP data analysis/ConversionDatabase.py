from array import * 
import numpy as np
import os
import pandas as pd

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



path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\5s-step\3D surface data\80Zdata.txt"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\5s-step\3D surface data"
filename =  os.path.splitext(os.path.split(path)[1])[0]
rawdata = np.loadtxt(path) 

# print(rawdata)
targetconversion = float(input("Please input the target conversion (%):"))
p = float(input("Please input the conversion deviation error (%):"))

findconversion = []
find_index = []
conresi = []

#Parameters used to calculate polymer concentration.
Vreactor = 1 # the volume of reactor is 1 ml
C_Monomer = 6 #float(input('\033[1;31mPlease input the initial concentration of your Monomer(M):>> \033[0m'))
C_RaftAgent = 0.5 #float(input('\033[1;31mPlease input the initial concentration of your RaftAgent (M):>> \033[0m'))
M_polymer = 0.5 # the molar of monomer needed

DesiredMn = 4000 # the desired molecular weight of polymer
Polymercon = []
TotalFlowrate = []
Timecomsumed = []
FlowMonomer = []; FlowRaft = []; FlowSolvent = []
VolumeMonomer = []; VolumeRaft = []; VolumeSolvent = []
Money = []
Efactor = []

Concentration = []
Residencetime = []
Conversion = []




for i in rawdata:
    for j in i:
        if np.absolute(j-targetconversion)*100/targetconversion <= p:
            findconversion.append(j)
            find_index.append(index_2d(rawdata,j))
            residencetime = (index_2d(rawdata,j)[0]* 5 + 60)/60
            flowrate = Vreactor/residencetime
            monomerconcentration = index_2d(rawdata,j)[1][0]* 0.0375 + 0.5 
            FRmonomer = monomerconcentration * flowrate / C_Monomer
            print(FRmonomer)
            FRraft = FRmonomer * C_Monomer / (100 * C_RaftAgent)
            FRSolvent = flowrate - FRmonomer - FRraft
            FlowMonomer.append(FRmonomer); FlowRaft.append(FRraft); FlowSolvent.append(FRSolvent)
            polymercon = monomerconcentration * (flowrate / 1000) * j/100 / ((DesiredMn - 350)/86.09)
            Polymercon.append(polymercon)
            Time_need = M_polymer/polymercon + 2
            # print(Time_need)
            Timecomsumed.append(Time_need)
            volumeMonomer = Time_need * FRmonomer
            volumeRaft = FRraft * Time_need
            volumeSolvent = FRSolvent * Time_need
            VolumeMonomer.append(volumeMonomer); VolumeRaft.append(volumeRaft); VolumeSolvent.append(volumeSolvent)
            MoneyConsumed = volumeMonomer* 0.032 + volumeRaft * 0.126 + volumeSolvent*0.0312   
            efactor = (volumeMonomer * 1 + volumeSolvent * 1.1 + volumeRaft *0.94137- 2000)/2000     
            Efactor.append(efactor)
            Money.append(MoneyConsumed)
            conresi.append([monomerconcentration,residencetime])
            Concentration.append(monomerconcentration)
            Residencetime.append(residencetime)
            TotalFlowrate.append(flowrate)

        else:
            pass

# save converison vaeries from time data to csv file
with open(r'{}\{}-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'Concentration/M':Concentration,
        'Residence time/minute':Residencetime,
        'Conversion/%':findconversion,
        'Polymerconcentration/ M/min':Polymercon,
        'TotalFlowrate/ ml/min':TotalFlowrate,
        'Timeconsumed/min':Timecomsumed,
        'FlowMonomer/ml/min':FlowMonomer, 'FlowRaft/ ml/min':FlowRaft, 'FlowSolvent/ ml/min': FlowSolvent,
        'VolumeMonomer/ ml':VolumeMonomer,'VolumerRaft/ ml':VolumeRaft, 'VolumeSolvent/ ml':VolumeSolvent,
        'Money/$':Money,
        'efactor':Efactor
}
        
column_names = ['Concentration/M','Residence time/minute','Conversion/%','Polymerconcentration/ M/min','TotalFlowrate/ ml/min','Timeconsumed/min',
                'FlowMonomer/ml/min', 'FlowRaft/ ml/min', 'FlowSolvent/ ml/min', 'VolumeMonomer/ ml', 'VolumerRaft/ ml', 'VolumeSolvent/ ml', 'Money/$','efactor'
]

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-Data.csv'.format(path_t,filename), columns = column_names)   

# print(findconversion)
# print()
# print(find_index)
# print()
# print(conresi)
# print()

        
 