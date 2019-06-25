""" Title: testign
    Purpose: 
        To Perform Tests on the datasets
        
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
import matplotlib.patches as mpatches

raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Baseline"
trim_type = 2
ws = 6
dm = 15 
zac = 600
zmc = 600
zlc = 600
ta = 20 

def get_protocol_program_parameters(RP, SI, sleep_param, param_index):
    """Gets the values for every data point for the specified sleep parameter

    """
    frag_program = []
    frag_protocol = []
    for part in RP:
        days = SI[part]
        i = 0
        while i < len(param_index[part]) and i < len(days):
            sleep_parameters = days[i]
            frag_part = sleep_parameters[sleep_param]
            frag_index_day = param_index[part]
            frag_program.append(frag_part)
            frag_protocol.append(frag_index_day[i])       
            i = i + 1
    
    return frag_program, frag_protocol

sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
protocol = ps.ProtocolSleepAnalysis(sa_directory, sleep_study.participant_list,
                                    study_name, assesment)
LOprotocol, GUprotocol, sleep_eff, frag_index, act_index, latency_index = protocol.get_study_analysis_sleep_times()



LO_one, GU_one, SI_one, PL_one = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta)
error, RP = err.get_error_study(LO_one,LOprotocol,PL_one)


LO_two, GU_two, SI_two, PL_two = sleep_study.get_in_bed_times(ws, 600, zmc, 10, zlc, ta)
LO_three, GU_three, SI_three, PL_three = sleep_study.get_in_bed_times(ws, 15, zmc, 10, zlc, ta)
LO_four, GU_four, SI_four, PL_four = sleep_study.get_in_bed_times(ws, dm, zmc + 15, zac, zlc, ta)
LO_five, GU_five, SI_five, PL_five = sleep_study.get_in_bed_times(ws, dm, zmc + 20, zac, zlc, ta)

fi_ula_one, fi_pro_one = get_protocol_program_parameters(RP, SI_one, 'Sleep efficiency %', sleep_eff)

fi_ula_two, fi_pro_two = get_protocol_program_parameters(RP, SI_two, 'Sleep efficiency %', sleep_eff)

fi_ula_three, fi_pro_three = get_protocol_program_parameters(RP, SI_three, 'Sleep efficiency %', sleep_eff)   

fi_ula_four, fi_pro_four = get_protocol_program_parameters(RP, SI_four, 'Sleep efficiency %', sleep_eff)   

fi_ula_five, fi_pro_five = get_protocol_program_parameters(RP, SI_five, 'Sleep efficiency %', sleep_eff)


ax = sns.distplot(fi_ula_one, color  = 'red', kde = True, hist = False)
sns.distplot(fi_ula_two, color = 'blue', kde = True, hist = False)
sns.distplot(fi_ula_three, color = 'purple', kde = True, hist = False)
#sns.distplot(fi_ula_four, color = 'orange', kde = True, hist = False)
#sns.distplot(fi_ula_five, color = 'gray', kde = True, hist = False)
sns.distplot(fi_pro_one, color = 'green', kde = True, hist = False)

ax.set_title('Sleep Effeciency Program and ULA Values')
ax.set_xlabel('Sleep Effeciency (%)')
ax.set_ylabel('Density')
ax.set_xlim(40, 100)

red_patch = mpatches.Patch(color='red', label='DM = 15')
blue_patch = mpatches.Patch(color='blue', label='ZAC = 10')
purple_patch = mpatches.Patch(color='purple', label='ZAC = 10, DM = 15')
#yellow_patch = mpatches.Patch(color='orange', label='DM = 20')
#gray_patch = mpatches.Patch(color='gray', label='DM = 25')
green_patch = mpatches.Patch(color='green', label='Sleep Protocol')

ax.legend(handles=[red_patch, blue_patch, purple_patch, green_patch ])


