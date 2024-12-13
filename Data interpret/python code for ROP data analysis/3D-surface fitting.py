import pandas as pd
import numpy as np
from array import * 
import os 
import csv
import matplotlib.pyplot as plt
import plotly
import scipy.linalg
import plotly.graph_objs as go
from mpl_toolkits import mplot3d
from string import ascii_uppercase
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score 


path = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\09. ROP\UsefulData\3. Useful data 20240327\3D-fitting data\30C\original_data.csv"
path_t = r"\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\09. ROP\UsefulData\3. Useful data 20240327\3D-fitting data\30C"
filename =  os.path.splitext(os.path.split(path)[1])[0]

with open(path) as csvfile:
    rawdata = list(csv.reader(csvfile, delimiter = ","))

exampledata = np.array(rawdata[1:],dtype = np.float64) 

X = exampledata[:,1]; Y = exampledata[:,2]; Z = exampledata[:,3]
data = np.c_[X,Y,Z]

def func(X, A, B, C, D, E, F, G, H, I, J):
    x,y,z = X.T 
    return (A*x**3 + B*y**3 + C*x*y**2 + D*y*x**2 + E*x**2 + F*y**2 + G*x*y + H*x + I*y + J)

popt, _ = curve_fit(func, data, data[:,2])

coefficient = []
for i, j in zip(popt, ascii_uppercase):
    print(f"{j} = {i:.3f}")
    coefficient.append(i)

# print(coefficient)

Zdata = coefficient[0]*X**3 + coefficient[1]*Y**3 + coefficient[2]*X*Y**2 + coefficient[3]*Y*X**2 + coefficient[4]*X**2 + coefficient[5]*Y**2 + coefficient[6]*X*Y + coefficient[7]*X + coefficient[8]*Y + coefficient[9]
data = np.c_[X,Y,Z]
residuals = Z - Zdata
ss_res = np.sum(residuals**2)
ss_tot = np.sum((Z-np.mean(Z))**2)
R_squared = 1 - (ss_res/ss_tot)
print(f"R_squared is {R_squared}")


fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1,2,1, projection='3d')
ax.scatter3D(X, Y, Z, c='r')
ax.set_xlabel('Concentration (M)')
ax.set_ylabel('Residence time (minute)')
ax.set_zlabel('Conversion (%)')
ax.set_title('Original Plot')

X, Y = np.meshgrid(X, Y)
zdata = coefficient[0]*X**3 + coefficient[1]*Y**3 + coefficient[2]*X*Y**2 + coefficient[3]*Y*X**2 + coefficient[4]*X**2 + coefficient[5]*Y**2 + coefficient[6]*X*Y + coefficient[7]*X + coefficient[8]*Y + coefficient[9]
ax = fig.add_subplot(1,2,2, projection='3d')
surf = ax.plot_surface(X, Y, zdata, cmap = plt.cm.rainbow, linewidth=0, antialiased=False, rcount=100, ccount=100)
ax.set_xlabel('DP')
ax.set_ylabel('Residence time (minute)')
ax.set_zlabel('Conversion (%)')
ax.set_title('Fitting Plot')
plt.savefig(f'{path_t}/{filename}')
plt.show()

