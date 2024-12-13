from csv import *
from turtle import color
import numpy as np
import pandas as pd
import csv
from math import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import plotly
from string import ascii_uppercase
from sklearn.metrics import r2_score 

path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA\5s-step\3D-fitting\FittingParameters.txt"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\07. Concentrationsweep\MA\5s-step\3D-fitting\reactionrate90"

T = float(input('\033[1;31mPlease input the temperature of your reaction (oC):>> \033[0m'))
if T == 80:
    n = 0

elif T == 90:
    n = 1

elif T == 100:
    n = 2

else:
    n = 3

rawdata = np.loadtxt(path) 
n = int(n)

Parameter = rawdata[:,n]
print(Parameter)



A = float(Parameter[0]); B = float(Parameter[1]); C = float(Parameter[2]); D = float(Parameter[3]); E = float(Parameter[4]); F = float(Parameter[5]); G = float(Parameter[6])
H = float(Parameter[7]); I = float(Parameter[8]); J = float(Parameter[9])

def func (x:float,y:float)->float:
    '''
    X: Concentration of monomer, unit: M; Y Residence time of reaction,unit:minute
    ''' 
    return(A*x**3 + B*y**3 + C*x*y**2 + D*y*x**2 + E*x**2 + F*y**2 + G*x*y + H*x + I*y + J)


def linearfit(residencetime:float,k)->float:
    '''
    linear fitting of kinetic data and get the slope of the fitting 
    '''
    return(k*residencetime)


# C_Monomer = float(input('\033[1;31mPlease input the concentration of your Monomer(M):>> \033[0m'))
# Residencetime = float(input('\033[1;31mPlease input the residencetime of your reaction (M):>> \033[0m'))

MonomerConcentration = []
Conversion = [] 
Kt = []
R2= []
Monomercon = []
Residence = []
Lnea = []

for i in range(16):

    C_Monomer = 0.5 + 0.3 *i
    MonomerConcentration.append(C_Monomer)
    Residencetime= []
    Lne = []
    Residencetime.append(0)
    Lne.append(0)
    for j in range(19):
        
        Monomercon.append(C_Monomer)
        residencetime = (60 + j*30)/60
        Residencetime.append(residencetime)
        Residence.append(residencetime)
        conversion = func(C_Monomer,residencetime)
        #Conversion.append(conversion)
        A0 = C_Monomer * (100-conversion)/100
        #print(A0)
        lne = np.log(A0/C_Monomer)
        #print(lne)
        Lne.append(lne)
        Lnea.append(lne)
        print(Lnea)
        with open(r'{}\{}-originalData.csv'.format(path_t, T), 'w') as f:
            pass 

        data = {
                'Monomerconcentration/M':Monomercon,
                'Residencetime':Residence,
                'lne':Lnea,
        }
                
        column_names = ['Monomerconcentration/M','Residencetime','lne']

        df = pd.DataFrame(data, columns = column_names) #columns = column_names
        df.to_csv(r'{}\{}-originalData.csv'.format(path_t,T), columns = column_names)    


    Residencetime = np.array(Residencetime)
    Residencetime = Residencetime[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(Residencetime, Lne, rcond=None)
    Ratecoefficient = abs(a[0])
    Kt.append(Ratecoefficient)
    data = a * Residencetime
    
    R_squared = r2_score(Lne, data)
    R2.append(R_squared)
    print(R_squared)
    
    plt.scatter(Residencetime, Lne, color = 'r')
    plt.plot(Residencetime, data, color = 'b')
    plt.xlabel('residencetime /minute')
    plt.ylabel('ln(M/MO)')
    plt.savefig(f'{path_t}/{C_Monomer}.png')
    plt.close()



# save converison vaeries from time data to csv file

with open(r'{}\{}-Data.csv'.format(path_t, T), 'w') as f:
    pass 
data = {
        'Monomerconcentration/M':MonomerConcentration,
        'Reactionrate':Kt,
        'R2 value':R2,
}
        
column_names = ['Monomerconcentration/M','Reactionrate','R2 value']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\{}-Data.csv'.format(path_t,T), columns = column_names)    