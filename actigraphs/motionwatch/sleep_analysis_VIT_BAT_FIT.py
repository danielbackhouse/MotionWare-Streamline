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

raw_data_directory = r"C:\Users\dbackhou\Desktop\FIT\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\FIT\VIT Sleep Diary.xlsx"
skiprows_rawdata = 20
study_name = "VIT"
assesment = "Baseline"
trim_type = 2
ws = 6
dm = 20 
zac = 10
zmc = 180
zlc = 180
ta = 20 

def get_parameter(SI, RP):
    FI_info = {}
    SE_info = {}
    SD_info = {}
    for participant in RP:
        participant_info = SI[participant]
        week_info_FI = []
        week_info_SE = []
        week_info_SD = []
        for day in participant_info:
            week_info_FI.append(day['Fragmentation Index'])
            week_info_SE.append(day['Sleep efficiency %'])
            week_info_SD.append(day['Actual sleep time'].total_seconds()/60)
        
        FI_info[participant] = week_info_FI
        SE_info[participant] = week_info_SE
        SD_info[participant] = week_info_SD
        
    return FI_info, SE_info, SD_info

def get_mean_param(SP, RP, index):
    mean_param = {}
    for participant in RP:
        mean_param[participant] = np.mean(SP[index][participant])
    
    return mean_param


def get_total_param(SP, RP, index):
    total_param = []
    for participant in RP:
        total_param += SP[index][participant]
             
    return total_param
        
        

# FIT Info
FIT_baseline = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)

FIT_baseline_info = FIT_baseline.get_in_bed_times(
        ws, dm, zmc, zac, zlc, ta)


raw_data_directory = r"C:\Users\dbackhou\Desktop\FIT\Midpoint"
assesment = "Midpoint"

FIT_midpoint = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)

FIT_midpoint_info = FIT_midpoint.get_in_bed_times(
        ws, dm, zmc, zac, zlc, ta)


# BAT Info
raw_data_directory = r"C:\Users\dbackhou\Desktop\BAT\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BAT\VIT Sleep Diary.xlsx"
assesment = "Baseline"
BAT_baseline = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
BAT_baseline_info = BAT_baseline.get_in_bed_times(
        ws, dm, zmc, zac, zlc, ta)


raw_data_directory = r"C:\Users\dbackhou\Desktop\BAT\Midpoint"
assesment = "Midpoint"

BAT_midpoint = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
BAT_midpoint_info = BAT_midpoint.get_in_bed_times(
        ws, dm, zmc, zac, zlc, ta)



FIT_B_SI = FIT_baseline_info[2]
FIT_M_SI = FIT_midpoint_info[2]
RP_FIT = ['095', '115', '120']


BAT_B_SI = BAT_baseline_info[2]
BAT_M_SI = BAT_midpoint_info[2]
RP_BAT = ['099', '103', '106', '107', '109']


BAT_baseline_SP = get_parameter(BAT_B_SI, RP_BAT)
BAT_midpoint_SP = get_parameter(BAT_M_SI, RP_BAT)

FIT_baseline_SP = get_parameter(FIT_B_SI, RP_FIT)
FIT_midpoint_SP = get_parameter(FIT_M_SI, RP_FIT)

# Per participant
FIT_B_SD_part = get_mean_param(FIT_baseline_SP, RP_FIT, 2)
FIT_M_SD_part = get_mean_param(FIT_midpoint_SP, RP_FIT, 2)

BAT_B_SD_part = get_mean_param(BAT_baseline_SP, RP_BAT, 2)
BAT_M_SD_part = get_mean_param(BAT_midpoint_SP, RP_BAT, 2)

FIT_B_SE_part = get_mean_param(FIT_baseline_SP, RP_FIT, 1)
FIT_M_SE_part = get_mean_param(FIT_midpoint_SP, RP_FIT, 1)

BAT_B_SE_part = get_mean_param(BAT_baseline_SP, RP_BAT, 1)
BAT_M_SE_part = get_mean_param(BAT_midpoint_SP, RP_BAT, 1)


# Per night
FIT_B_SD = get_total_param(FIT_baseline_SP, RP_FIT, 2)
FIT_M_SD = get_total_param(FIT_midpoint_SP, RP_FIT, 2)

BAT_B_SD = get_total_param(BAT_baseline_SP, RP_BAT, 2)
BAT_M_SD = get_total_param(BAT_midpoint_SP, RP_BAT, 2)

FIT_B_SE = get_total_param(FIT_baseline_SP, RP_FIT, 1)
FIT_M_SE = get_total_param(FIT_midpoint_SP, RP_FIT, 1)

BAT_B_SE = get_total_param(BAT_baseline_SP, RP_BAT, 1)
BAT_M_SE = get_total_param(BAT_midpoint_SP, RP_BAT, 1)

plt.figure()
plt.plot(FIT_B_SE, FIT_M_SE, 'ro')
plt.xlabel('FIT Baseline Sleep Effeciency')
plt.ylabel('FIT Midpoint Sleep Effeciency')
plt.title('Midpoint vs Baseline')


