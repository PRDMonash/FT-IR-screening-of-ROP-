from CreateDataFolder import *
import csv
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
import matplotlib.ticker
from matplotlib import rcParams
import matplotlib
matplotlib.use('Agg')
import os
import datetime
import pandas as pd
from numpy import sqrt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import matplotlib.ticker
from syringepump import *
from SF10 import *
from Functions import *
from datetime import datetime
import threading

# Create a experiment file folder to save all the data  
print("Please input the name of you Experiment :>>")
ExperimentName = input(':>>')
print("Please input the name of you FTIR Experiment :>>")
FTIRExperimentName = input(':>>')

# the path where we save the data
ParentFolder = r"S:\Sci-Chem\PRD\IR 112\Bo" 
Experimentfolder_path = CreateDataFolder(ExperimentName,ParentFolder)

# the path of IR rawdata, which will be monitored by watchdog 
IRrawdata_path = r"C:\Users\IR112\Documents\iC IR Experiments\{}".format(FTIRExperimentName) 
# the path in the shared drive where the IR raw data will be saved
SavedIRrawdata_path = r'{}/IR_RawData'.format(Experimentfolder_path) 

# create a empty csv file to save all the calsulated data 
with open(r'{}\{}-Data.csv'.format(Experimentfolder_path, ExperimentName), 'a') as f:
    pass 


# Open the reaction parameter file and load the data to data frame
ParameterFile_Path = r'S:\Sci-Chem\PRD\IR 112\Bo\PythonCode_ROP\CSExperimentParameter_Checking.xlsx'
  # copy the experiment parameters file to the experiment folder
shutil.copy(ParameterFile_Path, Experimentfolder_path)
Parameter_df =  pd.read_excel(ParameterFile_Path, index_col=0)
PumpName = Parameter_df.iloc[:,0]; PumpPort = Parameter_df.iloc[:,1]; StockConcentration = Parameter_df.iloc[:,2] 
Equvialent = Parameter_df.iloc[:,3]; QuenchingFlowRate = Parameter_df.iloc[:,4][3];DesiredMonomerCon = Parameter_df.iloc[:,8][1]
V_reactor = Parameter_df.iloc[:,5][1]; V_input = Parameter_df.iloc[:,6][1]; V_dead = Parameter_df.iloc[:,7][1]; dp = Parameter_df.iloc[:,10][1]
ResidenceTime = Parameter_df.iloc[:,9][1]

PumpMonmer = SyringePump(port=f'{PumpPort[1]}',name=f'{PumpName[1]}'); PumpCatalyst = SyringePump(port=f'{PumpPort[2]}',name=f'{PumpName[2]}')
PumpSolvent = SyringePump(port=f'{PumpPort[3]}',name=f'{PumpName[3]}')
#PumpQuenching = SF10(port=f'{PumpPort[4]}',name=f'{PumpName[4]}')


# Concentration sweep flow rate calculation
FlowRateMonomer = []; FlowRateCatalyst = []; FlowRateSolvent = []; DP = []; ConcentrationMonomer = []; SleepTime = []; MonomerCon =[]   
   # start point flow rate calculation
TotalFlowrate = V_reactor*60/ResidenceTime
FRMonomer =  TotalFlowrate*DesiredMonomerCon/StockConcentration[1]
FRCatalyst = TotalFlowrate* DesiredMonomerCon*Equvialent[2]/(Equvialent[1]*StockConcentration[2])
FRsolvent = TotalFlowrate-FRMonomer-FRCatalyst
FlowRateMonomer.append(FRMonomer); FlowRateCatalyst.append(FRCatalyst); FlowRateSolvent.append(FRsolvent); DP.append(dp)

ClearTime = V_reactor*60/TotalFlowrate + V_dead*60/(TotalFlowrate+QuenchingFlowRate)+60
SleepTime.append(ClearTime)

print(FlowRateMonomer)
print()
print(FlowRateCatalyst)
print()
print(FlowRateSolvent)
print()
print(SleepTime)
print()

PumpMonmer.start(); PumpCatalyst.start(); PumpSolvent.start(), #PumpQuenching.start()
sleep(0.5)
PumpMonmer.changeFlowrate(0);PumpCatalyst.changeFlowrate(0);PumpSolvent.changeFlowrate(0);#PumpQuenching.changeFlowrate(0)
sleep(0.5)

today = datetime.now()
CurrentTime = today.strftime("%H:%M:%S")
PumpMonmer.changeFlowrate(FRMonomer);PumpCatalyst.changeFlowrate(FRCatalyst)
PumpSolvent.changeFlowrate(FlowRateSolvent[0]);#PumpQuenching.changeFlowrate(QuenchingFlowRate)
sleep(SleepTime[0])
PumpMonmer.stop();PumpCatalyst.stop();PumpSolvent.stop();#PumpQuenching.stop()


