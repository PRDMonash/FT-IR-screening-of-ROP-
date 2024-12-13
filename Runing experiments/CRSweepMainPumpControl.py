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
from multiprocessing import Process

# Create a experiment file folder to save all the data  
print("Please input the name of you Experiment :>>")
ExperimentName = input(':>>')
print("Please input the name of you FTIR Experiment :>>")
FTIRExperimentName = input(':>>')

# the path where we save the data
ParentFolder =r"S:\Sci-Chem\PRD\IR 112\Bo"  
Experimentfolder_path = CreateDataFolder(ExperimentName,ParentFolder)

# the path of IR rawdata, which will be monitored by watchdog 
# IRrawdata_path = r"C:\Users\IR112\Documents\iC IR Experiments\{}".format(FTIRExperimentName) 
IRrawdata_path = r"S:\Sci-Chem\PRD\IR 112\Bo\2023\05\20\Congratulation\IR_RawData"

# the path in the shared drive where the IR raw data will be saved
SavedIRrawdata_path = r'{}/IR_RawData'.format(Experimentfolder_path) 

# create a empty csv file to save all the calsulated data 
with open(r'{}\{}-Data.csv'.format(Experimentfolder_path, ExperimentName), 'a') as f:
    pass 

# Open the reaction parameter file and load the data to data frame
ParameterFile_Path = r'S:\Sci-Chem\PRD\IR 112\Bo\PythonCode_ROP\CRSweepExperimentParameter.xlsx'
  # copy the experiment parameters file to the experiment folder
shutil.copy(ParameterFile_Path, Experimentfolder_path)
Parameter_df =  pd.read_excel(ParameterFile_Path, index_col=0)
PumpName = Parameter_df.iloc[:,0]; PumpPort = Parameter_df.iloc[:,1]; StockConcentration = Parameter_df.iloc[:,2] 
DesiredMonomerCon = Parameter_df.iloc[:,3][1]; QuenchingFlowRate = Parameter_df.iloc[:,4][3]; SweepRange = Parameter_df.iloc[:,8];  
V_reactor = Parameter_df.iloc[:,5][1]; V_input = Parameter_df.iloc[:,6][1]; V_dead = Parameter_df.iloc[:,7][1]; dp = Parameter_df.iloc[:,12][1]
SweepTimeLength = Parameter_df.iloc[:,9][1]; SweepStepLength = Parameter_df.iloc[:,10][1]; ResidenceTime = Parameter_df.iloc[:,11][1]

PumpMonmer = SyringePump(port=f'{PumpPort[1]}',name=f'{PumpName[1]}'); PumpCatalyst = SyringePump(port=f'{PumpPort[2]}',name=f'{PumpName[2]}')
PumpSolvent = SyringePump(port=f'{PumpPort[3]}',name=f'{PumpName[3]}')
# PumpQuenching = SF10(port=f'{PumpPort[4]}',name=f'{PumpName[4]}')

# Concentration sweep flow rate calculation
FlowRateMonomer = []; FlowRateCatalyst = []; FlowRateSolvent = []; DP = []; ConcentrationMonomer = []; SleepTime = []; MonomerCon =[]; CRatio= []   
# start point flow rate calculation
TotalFlowrate = V_reactor*60/ResidenceTime
FRMonomer =  TotalFlowrate*DesiredMonomerCon/StockConcentration[1]
FRCatalyst = TotalFlowrate* DesiredMonomerCon/(SweepRange[1]*StockConcentration[2])
FRsolvent = TotalFlowrate-FRMonomer-FRCatalyst
FlowRateMonomer.append(FRMonomer); FlowRateCatalyst.append(FRCatalyst); FlowRateSolvent.append(FRsolvent); DP.append(dp)

ClearTime = V_reactor*60/TotalFlowrate + V_dead*60/(TotalFlowrate+QuenchingFlowRate)+60
SleepTime.append(ClearTime)

# flow rate for the sweep experiments
SweepSteps = int(SweepTimeLength/SweepStepLength)
MCRDecreasingStep = (SweepRange[2]-SweepRange[1])/SweepSteps
MonomerCon.append(DesiredMonomerCon); DP.append(dp); CRatio.append(SweepRange[1])

for i in range(1,SweepSteps):
    CR = SweepRange[1]+i*MCRDecreasingStep
    FRCatalyst = TotalFlowrate**DesiredMonomerCon/(CR*StockConcentration[2])
    FRSolvent = TotalFlowrate-FRMonomer-FRCatalyst
    MonomerCon.append(DesiredMonomerCon);FlowRateMonomer.append(FRMonomer);FlowRateCatalyst.append(FRCatalyst)
    FlowRateSolvent.append(FRSolvent); DP.append(dp);SleepTime.append(SweepStepLength); CRatio.append(CR)

FRCatalyst = TotalFlowrate*DesiredMonomerCon/(SweepRange[2]*StockConcentration[2])
FRSolvent = TotalFlowrate - FRCatalyst- FRMonomer
MonomerCon.append(DesiredMonomerCon);FlowRateMonomer.append(FRMonomer); FlowRateCatalyst.append(FRCatalyst)
FlowRateSolvent.append(FRSolvent);SleepTime.append(ClearTime); CRatio.append(SweepRange[2])  

print(MonomerCon)
print()
print(FlowRateMonomer)
print()
print(FlowRateCatalyst)
print()
print(FlowRateSolvent)
print()
print(SleepTime)
print()
print(CRatio)
print()




PumpMonmer.start(); PumpCatalyst.start(); PumpSolvent.start()#, PumpQuenching.start()
sleep(0.5)
PumpMonmer.changeFlowrate(0);PumpCatalyst.changeFlowrate(0);PumpSolvent.changeFlowrate(0);#PumpQuenching.changeFlowrate(0)
sleep(0.5)
for i in range(SweepSteps+1):
    today = datetime.now()
    CurrentTime = today.strftime("%H:%M:%S")
    print(f"Changed to {i}/{SweepSteps} monomer concentration at {CurrentTime}")
    PumpMonmer.changeFlowrate(FlowRateMonomer[i]);PumpCatalyst.changeFlowrate(FlowRateCatalyst[i])
    PumpSolvent.changeFlowrate(FlowRateSolvent[i]);#PumpQuenching.changeFlowrate(QuenchingFlowRate)
    sleep(SleepTime[i])
PumpMonmer.stop();PumpCatalyst.stop();PumpSolvent.stop();#PumpQuenching.stop()


 