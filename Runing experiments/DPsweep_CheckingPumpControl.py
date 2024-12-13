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
ParameterFile_Path = r'S:\Sci-Chem\PRD\IR 112\Bo\PythonCode_ROP\DPSweepExperimentParameter_Checking.xlsx'
  # copy the experiment parameters file to the experiment folder
shutil.copy(ParameterFile_Path, Experimentfolder_path)
Parameter_df =  pd.read_excel(ParameterFile_Path, index_col=0)
PumpName = Parameter_df.iloc[:,0]; PumpPort = Parameter_df.iloc[:,1]; StockConcentration = Parameter_df.iloc[:,2] 
DesiredMonomerCon = Parameter_df.iloc[:,3][1]; QuenchingFlowRate = Parameter_df.iloc[:,4][3]; DesiredDP = Parameter_df.iloc[:,8][1];  
V_reactor = Parameter_df.iloc[:,5][1]; V_input = Parameter_df.iloc[:,6][1]; V_dead = Parameter_df.iloc[:,7][1]
SweepStepLength = Parameter_df.iloc[:,9][1]; ResidenceTime = Parameter_df.iloc[:,10][1]

PumpMonmer = SyringePump(port=f'{PumpPort[1]}',name=f'{PumpName[1]}'); PumpInitiator = SyringePump(port=f'{PumpPort[2]}',name=f'{PumpName[2]}')
PumpSolvent = SyringePump(port=f'{PumpPort[3]}',name=f'{PumpName[3]}')
# PumpQuenching = SF10(port=f'{PumpPort[4]}',name=f'{PumpName[4]}')

# Concentration sweep flow rate calculation
FlowRateMonomer = []; FlowRateInitiator = []; FlowRateSolvent = []; DP = []; ConcentrationMonomer = []; SleepTime = []; MonomerCon =[]   
   # start point flow rate calculation
TotalFlowrate = V_reactor*60/ResidenceTime
FRMonomer =  TotalFlowrate*DesiredMonomerCon/StockConcentration[1]
FRInitiator = TotalFlowrate*DesiredMonomerCon/(DesiredDP*StockConcentration[2])
FRsolvent = TotalFlowrate-FRMonomer-FRInitiator
dp = TotalFlowrate*DesiredMonomerCon/(FRInitiator*StockConcentration[2])
FlowRateMonomer.append(FRMonomer); FlowRateInitiator.append(FRInitiator); FlowRateSolvent.append(FRsolvent); DP.append(dp); MonomerCon.append(DesiredMonomerCon)

ClearTime = V_reactor*60/TotalFlowrate + V_dead*60/(TotalFlowrate+QuenchingFlowRate)+60
SleepTime.append(ClearTime)

print(MonomerCon)
print()
print(FlowRateMonomer)
print()
print(FlowRateInitiator)
print()
print(FlowRateSolvent)
print()
print(SleepTime)
print()
print(DP)




PumpMonmer.start(); PumpInitiator.start(); PumpSolvent.start(), #PumpQuenching.start()
sleep(0.5)
PumpMonmer.changeFlowrate(0);PumpInitiator.changeFlowrate(0);PumpSolvent.changeFlowrate(0); #PumpQuenching.changeFlowrate(0)
sleep(0.5)

today = datetime.now()
CurrentTime = today.strftime("%H:%M:%S")
PumpMonmer.changeFlowrate(FlowRateMonomer[0]);PumpInitiator.changeFlowrate(FlowRateInitiator[0])
PumpSolvent.changeFlowrate(FlowRateSolvent[0]); #PumpQuenching.changeFlowrate(QuenchingFlowRate)
sleep(SleepTime[0])
PumpMonmer.stop();PumpInitiator.stop();PumpSolvent.stop(); #PumpQuenching.stop()


