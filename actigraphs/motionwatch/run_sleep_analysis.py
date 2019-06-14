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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import seaborn as sns

raw_data_directory = r"C:\Users\dbackhou\Desktop\SC Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "SC"
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
LOprotocol, GUprotocol, sleep_eff, frag_index, act_index, latency_index = protocol.get_study_analysis_sleep_times()


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
       
# Fragmentation Index Error
frag_error = {}
frag_error_total = []
frag_error_per_total = []
frag_average_error = {}
frag_error_mean = []
frag_program = []
frag_protocol = []
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
        frag_program.append(frag_part)
        frag_protocol.append(frag_index_day[i])       
        i = i + 1

    frag_average_error[part] = sum(error)/len(error)
    frag_error[part] = error
    frag_error_total += error
    frag_error_mean  += mean
    frag_error_per_total += percent_error
    
sd = np.std(frag_error_total)
md = np.mean(frag_error_total)
vr = np.var(frag_error_total)

plt.figure(1)
plt.plot(frag_error_mean, frag_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot Fragmentation Index (SC)')
plt.xlabel('Mean Fragmentation Index')
plt.ylabel('Difference between Protocol and Program FI' )

plt.figure(2)
plt.text(70, 15, 'Pearson Correalation = 0.86', style = 'italic')
plt.text(70, 10, 'Spearman Correalation = 0.87', style = 'italic')
plt.text(20, 90, 'N = 2076', weight = 'bold', size = 'large')
plt.plot(frag_program, frag_protocol, 'bo')
plt.title('Plot of Protocol vs Program Fragmentation Index (SC)')
plt.xlabel('Program Fragnmentation Index')
plt.ylabel('Protocol Fragmentation Index')

# Sleep Effeciency Error    
eff_error = {}
eff_error_total = []
eff_error_mean = []
eff_program = []
eff_protocol = []
for part in RP:
    days = SI[part]
    error = []
    mean = []
    i = 0
    while i < len(sleep_eff[part]) and i < len(days):
        sleep_parameters = days[i]
        eff_part = sleep_parameters['Sleep efficiency %']
        eff_index_day = sleep_eff[part]
        error.append(eff_part - eff_index_day[i]) 
        mean.append((eff_part + eff_index_day[i])/2)
        eff_program.append(eff_part)
        eff_protocol.append(eff_index_day[i])
        i += 1
        
    eff_error[part] = error
    eff_error_total += error
    eff_error_mean += mean

    
sd = np.std(eff_error_total)
md = np.mean(eff_error_total)
vr = np.var(eff_error_total)

plt.figure(3)
plt.plot(eff_error_mean, eff_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot Sleep Effeciency (SC)')
plt.xlabel('Mean Sleep Effeciency')
plt.ylabel('Difference between Protocol and Program SE' )

plt.figure(4)
plt.text(60, 40, 'Pearson Correalation = 0.76', style = 'italic')
plt.text(60, 36, 'Spearman Correalation = 0.75', style = 'italic')
plt.text(40, 90, 'N = 2076', weight = 'bold', size = 'large')
plt.plot(eff_program, eff_protocol, 'bo')
plt.title('Plot of Protocol vs Program Sleep Effeciency (SC)')
plt.xlabel('Program Sleep Effeciency (%)')
plt.ylabel('Protocol Sleep Effeciency (%)')


# ACT Error    
act_error = {}
act_error_total = []
act_error_mean = []
act_program = []
act_protocol = []
for part in RP:
    days = SI[part]
    error = []
    mean = []
    i = 0
    while i < len(act_index[part]) and i < len(days):
        sleep_parameters = days[i]
        act_part = sleep_parameters['Actual sleep time']
        act_program_point = act_part.total_seconds()/60
        act_index_day = act_index[part]
        act_protocol_point = (act_index_day[i].hour*60 + act_index_day[i].minute)*60 + act_index_day[i].second
        error.append(act_program_point - act_protocol_point/60) 
        mean.append((act_program_point + act_protocol_point/60)/2)
        act_program.append(act_program_point)
        act_protocol.append(act_protocol_point/60)
        i += 1
        
    act_error[part] = error
    act_error_total += error
    act_error_mean += mean

    
sd = np.std(act_error_total)
md = np.mean(act_error_total)
vr = np.var(act_error_total)

plt.figure(5)
plt.plot(act_error_mean, act_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot Actual Sleep Time (SC)')
plt.xlabel('Mean Actual Sleep Time')
plt.ylabel('Difference between Protocol and Program AST' )

plt.figure(6)
plt.text(400, 140, 'Pearson Correalation = 0.85', style = 'italic')
plt.text(400, 120, 'Spearman Correalation = 0.86', style = 'italic')
plt.text(150, 550, 'N = 2076', weight = 'bold', size = 'large')
plt.plot(act_program, act_protocol, 'bo')
plt.title('Plot of Protocol vs Program Actual Sleep Time (SC)')
plt.xlabel('Program AST (min)')
plt.ylabel('Protocol AST (min)')

# Latency Error    
ly_error = {}
ly_error_total = []
ly_error_mean = []
ly_program = []
ly_protocol = []
for part in RP:
    days = SI[part]
    error = []
    mean = []
    i = 0
    while i < len(latency_index[part]) and i < len(days):
        sleep_parameters = days[i]
        ly_part = sleep_parameters['Sleep latency']
        ly_program_point = ly_part.total_seconds()/60
        ly_index_day = latency_index[part]
        ly_protocol_point = (ly_index_day[i].hour*60 + ly_index_day[i].minute)*60 + ly_index_day[i].second
        error.append(ly_program_point - ly_protocol_point/60) 
        mean.append((ly_program_point + ly_protocol_point/60)/2)
        ly_program.append(ly_program_point)
        ly_protocol.append(ly_protocol_point/60)
        i += 1
        
    ly_error[part] = error
    ly_error_total += error
    ly_error_mean += mean

    
sd = np.std(ly_error_total)
md = np.mean(ly_error_total)
vr = np.var(ly_error_total)

plt.figure(7)
plt.plot(ly_error_mean, ly_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot Sleep Latency (SC)')
plt.xlabel('Mean Sleep Latency (min)')
plt.ylabel('Difference between Protocol and Program Sleep Latency (min)' )

plt.figure(8)
plt.text(150, 140, 'Pearson Correalation = 0.26', style = 'italic')
plt.text(150, 130, 'Spearman Correalation = 0.14', style = 'italic')
plt.text(150, 120, 'P value (Spearman) = 1^-10')
plt.text(0, 140, 'N = 2076', weight = 'bold', size = 'large')
plt.plot(ly_program, ly_protocol, 'bo')
plt.title('Plot of Protocol vs Program Sleep latency (SC)')
plt.xlabel('Program Sleep Latency (min)')
plt.ylabel('Protocol Sleep Latency (min)')



data = np.array([eff_program, eff_protocol]).transpose()
df = pd.DataFrame(data, columns = ['SE program', 'SE protocol'])
eff_program_arr = np.array(eff_program)/sum(eff_program)
eff_protocol_arr = np.array(eff_protocol)/sum(eff_protocol)


ax = sns.distplot(eff_program, color  = 'red', kde = False)
sns.distplot(eff_protocol, color = 'blue', kde = False)
ax.set_title('Sleep Effeciency Distribution Program vs Protocol Values')
ax.set_xlabel('Sleep Effeciency Values')
ax.set_ylabel('Counts of Value')
ax.set_xlim(50, 100)

sns.jointplot(x = 'SE program', y = 'SE protocol', data = df)


