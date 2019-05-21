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
import create.ProtocolSleepAnalysis

raw_data_directory = r"C:\Users\dbackhou\Desktop\Bulk Raw Data Export BT\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\Bulk Raw Data Export BT\BT Sleep Diary.xlsx"
skiprows_rawdata = 20
study_name = "BT"
assesment = "Baseline"
trim_type = 2

sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)

#LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times()

#protocol = ps.ProtocolSleepAnalysis(participant_list, study_name, assesment)

#LOprotocol, GUprotocol = protocol.get_study_analysis_sleep_times()
