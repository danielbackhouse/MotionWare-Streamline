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

raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Final"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Final"
trim_type = 2
ws = 6
dm = 20 
zac = 10
zmc = 180
zlc = 180
ta = 20 
zsc = 10
lc = 10000

def get_ryan_info(sleep_info, participant_list):
    avg_sd = []
    avg_fi = []
    avg_se = []
    avg_sl = []
    avg_ws = []
    
    for participant in participant_list:
        participant_info = sleep_info[participant]
        fi = []
        sd = []
        se = []
        sl = []
        ws = []
        print(participant)
        for day_info in participant_info:
            if day_info != -1:
                fi.append(day_info['Fragmentation Index'])
                sd.append(day_info['Actual sleep time'].total_seconds()/60)
                se.append(day_info['Sleep efficiency %'])
                sl.append(day_info['Sleep latency'].total_seconds()/60)
                ws.append(day_info['Actual sleep time'].total_seconds()/60*(1-(day_info['Sleep efficiency %'])/100))
        
        avg_fi.append(np.mean(fi))
        avg_sd.append(np.mean(sd))
        avg_se.append(np.mean(se))
        avg_sl.append(np.mean(sl))
        avg_ws.append(np.mean(ws))
    
    sleep_data = [avg_fi, avg_sd, avg_se, avg_sl, avg_ws]
    df1 = pd.DataFrame(data = np.transpose(sleep_data), index = participant_list,
                       columns = ['frag index', 'actual sleep time', 'sleep efficieny', 'sleep latency', 'waso'])    
    return df1


# Get the times for the protocol and program
sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
LO, GU, SI, PL = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta, zsc, lc)

df1 = get_ryan_info(SI, PL)
df1.to_excel("BT_" + str(assesment) + "_updated.xlsx")
#protocol = ps.ProtocolSleepAnalysis(sa_directory, sleep_study.participant_list,
#                                    study_name, assesment)
#LOprotocol, GUprotocol, sleep_eff, frag_index, act_index, latency_index = protocol.get_study_analysis_sleep_times()

#error_study_GU, RP = err.get_error_study(GU,GUprotocol,PL)
#error_study_LO, RP = err.get_error_study(LO,LOprotocol,PL)