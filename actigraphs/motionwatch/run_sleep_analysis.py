""" Title: RUN_SLEEP_ANALYSIS
    Purpose: 
        *******************IMPORTANT PLEASE READ***************************
        This is the main program and SHOULD be used to run the sleep analysis
        (it should also be the only file you need to open).
        DO NOT make any changes to any of the other files within the program.
        It is recomondded that you only change the variables specified. There
        should be an explanation of what each variable does
        
    Author: Alan Yan and Daniel Backhouse
"""
import create.Study as study
import create.ProtocolSleepAnalysis as ps
import optimize.threshold_optimization as thresh
import compute.error_analysis as err
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Baseline"
trim_type = 2
ws = 6
dm = 12 
zac = 25
zmc = 180
zlc = 180
ta = 20 



# Get the times for the protocol and program
sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
LO, GU, SI, PL = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)

protocol = ps.ProtocolSleepAnalysis(sa_directory, sleep_study.participant_list,
                                    study_name, assesment)
LOprotocol, GUprotocol = protocol.get_study_analysis_sleep_times()


#get the error vaues
error_study_GU, RP = err.get_error_study(GU,GUprotocol,PL)
error_per_participant_GU = err.get_error_per_participant(GU, GUprotocol, PL)
count_GU = err.entries_over_fifteen(error_per_participant_GU)
error_GU = err.total_error(error_study_GU)

error_study_LO, RP = err.get_error_study(LO,LOprotocol,PL)
error_per_participant_LO = err.get_error_per_participant(LO, LOprotocol, PL)
count_LO = err.entries_over_fifteen(error_per_participant_LO)
error_LO = err.total_error(error_study_LO)

# compare to event markers
marker_dir = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline Markers"
marker_data = os.listdir(marker_dir)
markers = {}

for file in marker_data:
    if(file.endswith('.xlsx')):
        sheet = pd.read_excel(marker_dir + '\\' + file, skiprows = 16)
        dates = list(sheet.iloc[:,1])
        times = list(sheet.iloc[:,2])
        markers[file[3:6]] = [dates, times]
        
# create the plot space upon which to plot the data
fig, ax = plt.subplots(figsize = (10,10))

# add the x-axis and the y-axis to the plot
BT23 = markers['013']
BT23Program = LO['023']

LOdates = []
LOtimes = []
for dateTime in BT23Program:
    LOdates.append(dateTime.date())
    LOtimes.append(dateTime.time())
    


ax.plot(BT23[0], 
        BT23[1], 
        'ro')

ax.plot(LOdates, LOtimes, 'bs')
#ax.plot(BT23[0], datetime.time(3,0,0))
#ax.set_ylim([datetime.time(3, 0, 0), datetime.time(1, 0, 0)])
# rotate tick labels
plt.setp(ax.get_xticklabels(), rotation=45)

# set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Time",
       title="Times vs Date");

