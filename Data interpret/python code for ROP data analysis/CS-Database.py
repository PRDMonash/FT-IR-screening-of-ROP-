from array import * 
import numpy as np
import os
import pandas as pd

def Calresidue(targetconversion,x,y)->float:
    '''
    Explanation: this function is used to calculate the residence time
    '''
    residue = abs(0- targetconversion + 0.246*y**3 -0.001 *x*y - 5.007*y**2 + 0.002*x*y + 0.251*x+ 36.721*y- 29.385)

    return(residue)

path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA-DPSWEEP\3D sureface plot\100C-matrix.txt"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA-DPSWEEP\3D sureface plot"
filename =  os.path.splitext(os.path.split(path)[1])[0]
rawdata = np.loadtxt(path) 

# print(rawdata)
findconversion = []
find_index = []
conresi = []

#Parameters used to calculate polymer concentration.
Vreactor = 1 # the volume of reactor is 1 ml
C_Monomer = 6 #float(input('\033[1;31mPlease input the initial concentration of your Monomer(M):>> \033[0m'))
C_RaftAgent = 0.5 #float(input('\033[1;31mPlease input the initial concentration of your RaftAgent (M):>> \033[0m'))
C_Initiator = 0.05 #float(input('\033[1;31mPlease input the initial concentration of your initiator (M):>> \033[0m'))
M_polymer = 0.5 # the molar of monomer needed

DesiredMn = 4000 # the desired molecular weight of polymer
targetdp = (DesiredMn - 350)/86.09

Polymercon = []
TotalFlowrate = []
Timecomsumed = []
FlowMonomer = []; FlowRaft = []; FlowSolvent = []; FlowInitiator = []
VolumeMonomer = []; VolumeRaft = []; VolumeSolvent = []; VolumeInitiator = []
Money = []
Efactor = []

DP = []
Residencetime = []
Conversion = []




for dp in range(50,171):
    for i in range(541):
        time = (60 + i *1)/60
        targetconversion = targetdp*100/dp
        left = Calresidue(targetconversion, dp, time)

        if  left <= 0.05: 
            residencetime = time
            print(f"DP is {dp}" )
            print (residencetime)
            Conversion.append(targetconversion)
            DP.append(dp)
            flowrate = Vreactor/residencetime     
            FRmonomer = 3 * flowrate / C_Monomer
            print(f"monomer flow rate is {FRmonomer}")
            FRraft = FRmonomer * C_Monomer / (dp * C_RaftAgent)
            FRInitiator = 3 * flowrate / C_Monomer/ 1000 
            FRSolvent = flowrate - FRmonomer - FRraft - FRInitiator 
            FlowMonomer.append(FRmonomer); FlowRaft.append(FRraft); FlowSolvent.append(FRSolvent); FlowInitiator.append(FRInitiator)
            polymercon = 3 * (flowrate / 1000) * targetconversion/100 / ((DesiredMn - 350)/86.09)
            Polymercon.append(polymercon)
            Time_need = M_polymer/polymercon + 2
            # print(Time_need)
            Timecomsumed.append(Time_need)
            volumeMonomer = Time_need * FRmonomer
            volumeRaft = FRraft * Time_need
            volumeSolvent = FRSolvent * Time_need
            volumeInitiator = FRInitiator * Time_need
            VolumeMonomer.append(volumeMonomer); VolumeRaft.append(volumeRaft); VolumeSolvent.append(volumeSolvent); VolumeInitiator.append(volumeInitiator)
            MoneyConsumed = volumeMonomer* 0.032 + volumeRaft * 0.95 + volumeSolvent * 0.0312 + volumeInitiator * 0.11902
            efactor = (volumeMonomer * 1 + volumeSolvent * 1.1 + volumeRaft *0.94137 + volumeInitiator * 1.11 - DesiredMn*M_polymer)/(DesiredMn*M_polymer)     
            Efactor.append(efactor)
            Money.append(MoneyConsumed)
            conresi.append([dp,residencetime])
            Residencetime.append(residencetime)
            TotalFlowrate.append(flowrate)
        else:
            pass

# save converison vaeries from time data to csv file
with open(r'{}\{}-calculation-Data.csv'.format(path_t, filename), 'w') as f:
    pass 
data = {
        'DP/M':DP,
        'Conversion/%':Conversion,
        'Residence time/minute':Residencetime,
        'Polymerconcentration/ M/min':Polymercon,
        'TotalFlowrate/ ml/min':TotalFlowrate,
        'Timeconsumed/min':Timecomsumed,
        'FlowMonomer/ml/min':FlowMonomer, 'FlowRaft/ ml/min':FlowRaft, 'FlowSolvent/ ml/min': FlowSolvent, 'FlowInitiator/ ml/min': FlowInitiator,
        'VolumeMonomer/ ml':VolumeMonomer,'VolumerRaft/ ml':VolumeRaft, 'VolumeSolvent/ ml':VolumeSolvent,'VolumeInitiator/ ml':VolumeInitiator,
        'Money/$':Money,
        'efactor':Efactor
}
        
print(len(DP))
print(len(Residencetime))
print(len(Polymercon))
print(len(TotalFlowrate))
print(len(Timecomsumed))
print(len(FlowMonomer))
print(len(VolumeMonomer))
print(len(Money))
print(len(Efactor))




column_names = ['DP/M','Conversion/%','Residence time/minute','Polymerconcentration/ M/min','TotalFlowrate/ ml/min','Timeconsumed/min',
                'FlowMonomer/ml/min', 'FlowRaft/ ml/min', 'FlowSolvent/ ml/min', 'FlowInitiator/ ml/min', 'VolumeMonomer/ ml', 'VolumerRaft/ ml', 'VolumeSolvent/ ml', 'VolumeInitiator/ ml', 'Money/$','efactor'
]

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-calculation-Data.csv'.format(path_t,filename), columns = column_names)   

# print(findconversion)
# print()
# print(find_index)
# print()
# print(conresi)
# print()

        
 