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
import compute.sleep_analysis as sleep_analysis
import create.ProtocolSleepAnalysis as ps
import compute.error_analysis as err
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.patches as mpatches
import datetime

raw_data_directory = r"C:\Users\dbackhou\Desktop\SC Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "SC"
assesment = "Baseline"
trim_type = 2
ws = 6
dm = 20 
zac = 10
zmc = 180
zlc = 180
ta = 20 

    

def plot_correlation_graph(x, y, xtitle, ytitle, title, xpos, ypos):
    """ Plots the correlation plots between two quantities and gives the spearman
    and pearson correlation between the two
    """
    pears = pearsonr(x, y)

    plt.figure()
    plt.text(xpos, ypos, 'Pearson Correalation = ' + str(round(pears[0],2)), style = 'italic')
    #plt.text(xpos, ypos-5, 'Spearman Correalation = ' + str(round(spear[0],2)), style = 'italic')
    #plt.text(20, 90, 'N = ' + str(len(x)), weight = 'bold', size = 'large')
    plt.plot(x, y, 'bo')
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    
def get_parameter_info(program_SI, protocol_PI, RP, parameter):
    """" Gets info on important paramters, passed program sleep info
    and protocol parameter info and the relevant participants
    """
    error_total = []
    error_mean = []
    program = []
    protocol = []
    part_program = []
    part_protocol = []
    
    for participant in RP:
        param_program = program_SI[participant]
        param_protocol = protocol_PI[participant]
        program_sum = 0
        protocol_sum = 0
        i = 0
        while i < len(param_protocol) and i < len(param_program):
            day_sleep_info = param_program[i]
            param_ULA = day_sleep_info[parameter]
            param_human = param_protocol[i]
            error_total.append(param_ULA - param_human) 
            error_mean.append((param_ULA + param_human)/2)
            program.append(param_ULA)
            protocol.append(param_human)
            program_sum += param_ULA
            protocol_sum += param_human
            i = i + 1
        part_program.append(program_sum/(i))
        part_protocol.append(protocol_sum/(i))
    return program, part_program, protocol, part_protocol, error_mean, error_total

def plot_bland_altman(error_total, mean_error, xtitle, ytitle, title):
    sd = np.std(error_total)
    md = np.mean(error_total)
    
    plt.figure()
    plt.plot(mean_error, error_total, 'ro')
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)


# Get the times for the protocol and program
sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
LO, GU, SI, PL = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)

protocol = ps.ProtocolSleepAnalysis(sa_directory, sleep_study.participant_list,
                                    study_name, assesment)
LOprotocol, GUprotocol, sleep_eff, frag_index, act_index, latency_index = protocol.get_study_analysis_sleep_times()

error_study_GU, RP = err.get_error_study(GU,GUprotocol,PL)
error_study_LO, RP = err.get_error_study(LO,LOprotocol,PL)

       
frag_info = get_parameter_info(SI, frag_index, RP, 'Fragmentation Index') 

plot_bland_altman(frag_info[5], frag_info[4], 'Mean Fragmentation Index',
                  'Difference between Protocol and ULA FI', 
                  'Bland Altman Plot Fragmentation Index (SC)' )
    

plot_correlation_graph(frag_info[0], frag_info[2],
                       'Program Fragnmentation Index','ULA Fragmentation Index',
                       'Plot of ULA vs Program Fragmentation Index (SC)', 50, 15 )

plot_correlation_graph(frag_info[1], frag_info[3],
                       'Program Fragnmentation Index','ULA Fragmentation Index',
                       'Plot of ULA vs Program Fragmentation Index (SC)', 50, 15 )



eff_info = get_parameter_info(SI, sleep_eff, RP, 'Sleep efficiency %') 

plot_bland_altman(eff_info[5], eff_info[4], 'Mean Sleep Effeciency',
                  'Difference between Protocol and ULA SE', 
                  'Bland Altman Plot Sleep Effeciency (SC)' )
    

plot_correlation_graph(eff_info[0], eff_info[2],
                       'Program Fragnmentation Index','ULA Fragmentation Index',
                       'Plot of ULA vs Program Fragmentation Index (SC)', 60, 40 )

plot_correlation_graph(eff_info[1], eff_info[3],
                       'Program Fragnmentation Index','ULA Fragmentation Index',
                       'Plot of ULA vs Program Fragmentation Index (SC)', 70, 60 )


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

pears = pearsonr(act_program, act_protocol)
spear = spearmanr(act_program, act_protocol)

plt.figure(5)
plt.plot(act_error_mean, act_error_total, 'ro')
plt.axhline(md,           color='gray', linestyle='--')
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
plt.title('Bland Altman Plot Actual Sleep Time (SC)')
plt.xlabel('Mean Actual Sleep Time')
plt.ylabel('Difference between Protocol and ULA AST' )

plt.figure(6)
plt.text(300, 140, 'Pearson Correalation = '  + str(round(pears[0],2)), style = 'italic')
plt.text(300, 120, 'Spearman Correalation = ' + str(round(spear[0],2)), style = 'italic')
plt.text(150, 550, 'N = ' + str(len(act_program)), weight = 'bold', size = 'large')
plt.plot(act_program, act_protocol, 'bo')
plt.title('Plot of Protocol vs ULA Actual Sleep Time (SC)')
plt.xlabel('ULA AST (min)')
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
plt.ylabel('Difference between Protocol and ULA Sleep Latency (min)' )

plt.figure(8)
plt.text(150, 140, 'Pearson Correalation = 0.26', style = 'italic')
plt.text(150, 130, 'Spearman Correalation = 0.14', style = 'italic')
plt.text(0, 140, 'N = 2076', weight = 'bold', size = 'large')
plt.plot(ly_program, ly_protocol, 'bo')
plt.title('Plot of Protocol vs ULA Sleep latency (SC)')
plt.xlabel('ULA Sleep Latency (min)')
plt.ylabel('Protocol Sleep Latency (min)')



file = pd.read_excel(r"C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Complete Diary.xlsx", 
                     sheet_name = None)

LO_diary = {}
GU_diary = {}
midnight = datetime.time(0, 0)
midday  = datetime.time(16, 0)
diary_participants = []
for participants in RP:
    if ('SC-'+ participants) in file.keys():
        diary_participants.append(participants)
        sheet = file['SC-' + participants]
        dates = list(sheet)
        dates.pop()
        dates.reverse()
        dates.pop()
        dates.reverse()
        
        LO_times =  sheet.iloc[1, 1:15].tolist()
        LO_times_fixed = []  
        for i in range(0,len(LO_times)):
            time = LO_times[i]
            if isinstance(time, datetime.datetime):
                time = time.time()
                
            if(time > midnight and time < midday):
                LOdatetime = datetime.datetime.combine(
                        dates[i] + datetime.timedelta(days = 1), time)
                LO_times_fixed.append(LOdatetime)
            else:
                LOdatetime = datetime.datetime.combine(
                        dates[i], time)
                LO_times_fixed.append(LOdatetime)
            
        LO_diary[participants] = LO_times_fixed
        
    
        GU_times = sheet.iloc[6, 1:15].tolist()
        GU_times_fixed = []   
        for i in range(0, len(GU_times)):
            time = GU_times[i]
            if isinstance(time, datetime.datetime):
                time = time.time()
            
            GUdatetime = datetime.datetime.combine(dates[i], time)
            GU_times_fixed.append(GUdatetime)   
        GU_diary[participants] = GU_times_fixed
        
        
    
#TODO: Do something with the returned dictionary
sleepAnalysisInfo = sleep_analysis.findSleepAnalysisData(
        activity[lights_out_index: got_up_index], 
                   dateTimes[lights_out_index: got_up_index])


