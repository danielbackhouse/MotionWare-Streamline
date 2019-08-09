# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:24:13 2019

@author: dbackhou
"""

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

raw_data_directory = r"C:\Users\dbackhou\Desktop\VIT Grant\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\VIT Grant\VIT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\SC Sleep Copy\SC Sleep Analysis.xlsx'
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
zsc = 10
lc = 10000


# Get the times for the protocol and program
sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
LO, GU, SI, PL = sleep_study.get_in_bed_times(ws, dm, zmc, zac, zlc, ta, zsc, lc)



raw_data_directory = r"C:\Users\dbackhou\Desktop\VIT Grant\Final"
assesment = "Final"


sleep_study_midpoint = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)
LO_mid, GU_mid, SI_mid, PL_mid = sleep_study_midpoint.get_in_bed_times(ws, dm, zmc, zac, zlc, ta, zsc, lc)

