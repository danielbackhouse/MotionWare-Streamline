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

plt.figure('Lights Out Error')
err.plot_study_error(error_study_LO, RP)
plt.figure('Got Up Error')
err.plot_study_error(error_study_GU, RP)

total_list = []
plt.figure('Plot of all Points for each day')
for participant in list(error_per_participant_GU.values()):
    plt.plot(participant, 'bo')
    total_list += participant
 
plt.figure('Plot of all points GU')
plt.plot(total_list, 'bo')
plt.plot(markersize = 1)
plt.xlabel('Time point')
plt.ylabel('Absolute error in minutes')
plt.title('Absolute error vs Time Points')

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
pid = '092'
BT23 = markers[pid]
BT23ProgramLO = LO[pid]
BT23ProgramGU = GU[pid]
BT23ProtocolLO = LOprotocol[pid]
BT23ProtocolGU = GUprotocol[pid]

LOdates = []
LOtimes = []
for dateTime in BT23ProgramLO:
    LOdates.append(dateTime.date())
    LOtimes.append(dateTime.time())

GUdates = []
GUtimes = []  
for dateTime in BT23ProgramGU:
    GUdates.append(dateTime.date())
    GUtimes.append(dateTime.time())

LOdatespro = []
LOtimespro = []
for dateTime in BT23ProtocolLO:
    LOdatespro.append(dateTime.date())
    LOtimespro.append(dateTime.time())

GUdatespro = []
GUtimespro = []  
for dateTime in BT23ProtocolGU:
    GUdatespro.append(dateTime.date())
    GUtimespro.append(dateTime.time())



ax.plot(BT23[0], BT23[1], 'rs')
ax.plot(LOdates, LOtimes, 'bo')
ax.plot(GUdates, GUtimes, 'bo')
ax.plot(LOdatespro, LOtimespro, 'g^')
ax.plot(GUdatespro, GUtimespro, 'g^')
# rotate tick labels
plt.xlim([BT23[0], BT23[-1]])
#plt.setp(rotation=45)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)
# set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Time",
       title="Times vs Date");

