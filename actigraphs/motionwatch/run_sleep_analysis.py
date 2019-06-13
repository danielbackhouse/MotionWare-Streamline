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
import compute.error_analysis as err
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Final"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Final"
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
LOprotocol, GUprotocol, sleep_eff, frag_index = protocol.get_study_analysis_sleep_times()


# Get the absolute errors between the two
error_study_GU, RP = err.get_error_study(GU,GUprotocol,PL)
error_per_participant_GU = err.get_error_per_participant(GU, GUprotocol, PL)
count_GU = err.entries_over_fifteen(error_per_participant_GU)
error_GU = err.total_error(error_study_GU)

error_study_LO, RP = err.get_error_study(LO,LOprotocol,PL)
error_per_participant_LO = err.get_error_per_participant(LO, LOprotocol, PL)
count_LO = err.entries_over_fifteen(error_per_participant_LO)
error_LO = err.total_error(error_study_LO)

# Plot the relative errors of GU and LO
plt.figure('Lights Out Error')
err.plot_study_error(error_study_LO, RP)
plt.figure('Got Up Error')
err.plot_study_error(error_study_GU, RP)

total_list = []
for participant in list(error_per_participant_GU.values()):
    total_list += participant
 
plt.figure('Plot of all points GU')
plt.plot(total_list, 'bo')
plt.plot(markersize = 1)
plt.xlabel('Time point')
plt.ylabel('Absolute error in minutes')
plt.title('Absolute error vs Time Points')


# Find the Event marker times
#marker_dir = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline Markers"
#marker_data = os.listdir(marker_dir)
#markers = {}
#for file in marker_data:
#    if(file.endswith('.xlsx')):
#        sheet = pd.read_excel(marker_dir + '\\' + file, skiprows = 16)
#        dates = list(sheet.iloc[:,1])
#        times = list(sheet.iloc[:,2])
#        markers[file[3:6]] = [dates, times]

        
# Event Marker Plot
#fig, ax = plt.subplots(figsize = (10,10))
#pid = '092'
#BT23 = markers[pid]
#BT23ProgramLO = LO[pid]
#BT23ProgramGU = GU[pid]
#BT23ProtocolLO = LOprotocol[pid]
#BT23ProtocolGU = GUprotocol[pid]

#LOdates = []
#LOtimes = []
#for dateTime in BT23ProgramLO:
#    LOdates.append(dateTime.date())
#    LOtimes.append(dateTime.time())

#GUdates = []
#GUtimes = []  
#for dateTime in BT23ProgramGU:
#    GUdates.append(dateTime.date())
#    GUtimes.append(dateTime.time())

#LOdatespro = []
#LOtimespro = []
#for dateTime in BT23ProtocolLO:
#    LOdatespro.append(dateTime.date())
#    LOtimespro.append(dateTime.time())

#GUdatespro = []
#GUtimespro = []  
#for dateTime in BT23ProtocolGU:
#    GUdatespro.append(dateTime.date())
#    GUtimespro.append(dateTime.time())

#ax.plot(BT23[0], BT23[1], 'rs')
#ax.plot(LOdates, LOtimes, 'bo')
#ax.plot(GUdates, GUtimes, 'bo')
#ax.plot(LOdatespro, LOtimespro, 'g^')
#ax.plot(GUdatespro, GUtimespro, 'g^')
#plt.xticks(fontsize=10, rotation=45)
#plt.yticks(fontsize=10)
#ax.set(xlabel="Date",ylabel="Time", title="Times vs Date");

       
# Fragmentation Index Error
frag_error = {}
frag_error_total = []
frag_error_per_total = []
frag_average_error = {}
frag_error_mean = []
for part in RP:
    days = SI[part]
    error = []
    percent_error = []
    mean = []
    sum_frag_com = 0
    sum_frag_hum = 0
    i = 0
    while i < len(frag_index[part]) and i < len(days):
        sleep_parameters = days[i]
        frag_part = sleep_parameters['Fragmentation Index']
        frag_index_day = frag_index[part]
        error.append(frag_part - frag_index_day[i]) 
        percent_error.append(((frag_part-frag_index_day[i])/frag_index_day[i])*100)
        sum_frag_com += frag_part
        sum_frag_hum += frag_index_day[i]
        mean.append((frag_part + frag_index_day[i])/2)
        i = i + 1
        
    frag_average_error[part] = sum(error)/len(error)
    frag_error[part] = error
    frag_error_total += error
    frag_error_mean  += mean
    frag_error_per_total += percent_error
    
# Sleep Effeciency Error    
#eff_error = {}
#eff_error_total = []
#for part in RP:
#    days = SI[part]
#    error = []
#    for i in range(0, len(frag_index[part])):
#        sleep_parameters = days[i]
#        eff_part = sleep_parameters['Sleep efficiency %']
#        eff_index_day = sleep_eff[part]
#        error.append(eff_part - eff_index_day[i]) 
#        
#    eff_error[part] = error
#    eff_error_total += error

plt.figure('Fragmentation Index Error')
plt.plot(frag_error_total, 'bo')     

#plt.figure('Sleep Efficiency % Error')
#plt.plot(eff_error_total, 'bo')     

plt.figure('Fragmentation Index Percent Error')
plt.plot(frag_error_per_total, 'bo')

plt.figure('Average Fragmentation error per participant')
plt.plot(list(frag_average_error.keys()),list(frag_average_error.values()), 'g^')
plt.xticks(rotation=90)

#Sleep Diary Review
#diary_quality = [ 0, 0, 10, 1, 2, 1, 2, 1, 0, 4, 3, 5, 4, 5, 1, 2, 3, 0, 10, 3,
#                 1, 1, 5, 8, 1, 9, 1, 8, 0, 0, 2, 2, 0, 0, 0, 0, 2, 3, 1, 0, 1, 9, 6,
#                 1, 3, 0, 4, 1, 1, 2, 1, 0, 0, 1, 4, 0, 2, 6, 1, 0, 3, 0, 1, 0, 1, 0,
#                 1, 0, 0, 2]
#diary_qual = {}
#for i in range(0,len(RP)):
#    diary_qual[RP[i]] = diary_quality[i]
    
    
#plt.figure('sleep diary quality')
#plt.plot(list(error_study_LO.values()), diary_quality, 'ro')

#large_error_LO = {}
#large_error_GU = {}
#large_diary_GU = {}
#large_diary_LO = {}
#for part in RP:
#    if(error_study_LO[part] > 20):
#        large_error_LO[part] = error_study_LO[part]
#        large_diary_LO[part] = diary_qual[part]
#    
#    if(error_study_GU[part] > 20):
#        large_error_GU[part] = error_study_GU[part]
#        large_diary_GU[part] = diary_qual[part]
    
#plt.figure('sleep diary quality for large error')
#plt.title('Sleep Diary Quality vs Absolute LO time error > 20min/day')
#plt.plot(list(large_error_LO.values()), list(large_diary_LO.values()), 'ro')   
#plt.xlabel('Absolute Error in min/day')
#plt.ylabel('Sleep Diary Quality Score')

sd = np.std(frag_error_total)
md = np.mean(frag_error_total)
vr = np.var(frag_error_total)

plt.figure('Bland Altman Plot')
plt.plot(frag_error_mean, frag_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot')
plt.xlabel('Mean Fragmentation Index')
plt.ylabel('Difference between Protocol and Program FI' )