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
import Study
import ProtocolSleepAnalysis as ps
import pandas as pd
# Raw Data Directory: THIS IS A REQUIRED FIELD. Enter the directory where the 
# raw data files are located. The raw data files should be in folders Baseline
# Midpoint and Final
raw_data_directory = r"C:\Users\dbackhou\Desktop\Bulk Raw Data Export BT\Baseline"

# SkipRows Raw Data: THIS IS A REQUIRED FIELD. This field should not be changed 
# unless the format of the raw data files has changed. This field is the most
# likely to vary between study
skiprows_rawdata = 20

# study_name: THIS IS A REQUIRED FIELD. Enter within the qoutations the
# abbreviation of the study. An example entry would be: "BT" or "FACT".
study_name = "BT"

# assesment: THIS A REQUIRED FIELD. Enter whether you want to analyze Baseline,
# Midpoint or Final. Valid entries then are: "Baseline", "Midpoint", "Final."
assesment = "Baseline"

# *************DO NOT MAKE CHANGES TO THE PROGRAM BEYOND THIS POINT**********

sleep_study = Study.Study(raw_data_directory, skiprows_rawdata, study_name, assesment)

LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times()

protocol = ps.ProtocolSleepAnalysis(participant_list, study_name, assesment)

LOprotocol, GUprotocol = protocol.get_study_analysis_sleep_times()

for i in range(0, len(LOprotocol)):
    protocolDates = LOprotocol[i]
    dates = LOdates[i]
    print(i)
    if(protocolDates[0].date() < dates[0].date()):
        print('f')





