import pandas as pd
import numpy as np
import math
from sklearn.metrics import r2_score



def func(T,Ea,A):
    """
    this function is defined to fitting the Arrhenius equation
    k: is the observed reation rate,
    T: is the reaction temperature, unit is K
    """
    return (Ea*1/T+A)

T = [1/273.15, 1/283.15, 1/293.15, 1/303.15, 1/308.15]


kinectic_data_file_path = r'\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\09. ROP\UsefulData\5. Useful data -final data\activation_energy\kineticdata.xlsx'

kinetic_data = pd.read_excel(kinectic_data_file_path)
concen_list = kinetic_data.iloc[:,0]; kobs_0 = kinetic_data.iloc[:,1];kobs_10 = kinetic_data.iloc[:,2];kobs_20 = kinetic_data.iloc[:,3];kobs_30 = kinetic_data.iloc[:,4];kobs_35 = kinetic_data.iloc[:,5]

Con_list = []; Ea_list = []; A_list = []; R2 = []; 
for i in range(31):
    Y = []
    Y.append(math.log(kobs_0[i]))
    Y.append(math.log(kobs_10[i]))
    Y.append(math.log(kobs_20[i]))
    Y.append(math.log(kobs_30[i]))
    Y.append(math.log(kobs_35[i]))
    
    """fitting part"""
    X = np.array(T)
    Y = np.array(Y)
    fitting_results = np.polyfit(X,Y, deg=1)
    print(fitting_results)
    Ea = abs(fitting_results[0])*8.314; A = math.exp(fitting_results[1])
    predict = np.poly1d(fitting_results)
    R =r2_score(Y,predict(X)) 

    Con_list.append(concen_list[i]); Ea_list.append(Ea); A_list.append(A);R2.append(R)



path = r'\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\09. ROP\UsefulData\5. Useful data -final data\activation_energy'
with open(r'{}\fittingresults.csv'.format(path), 'w') as f:
    pass 

data = {
        'Concentration':Con_list,
        'Ea':Ea_list,
        'A':A_list,
        'R2':R2
}
        
column_names = ['Concentration','Ea','A','R2']

df = pd.DataFrame(data, columns = column_names) #columns = column_names
df.to_csv(r'{}\fittingresults.csv'.format(path), columns = column_names)  

    