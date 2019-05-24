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
    

raw_data_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\Baseline"
sleep_diary_directory = r"C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Diary.xlsx"
sa_directory =  r'C:\Users\dbackhou\Desktop\BT Sleep Copy\BT Sleep Analysis.xlsx'
skiprows_rawdata = 20
study_name = "BT"
assesment = "Baseline"
trim_type = 2

sleep_study = study.Study(raw_data_directory, skiprows_rawdata, study_name,
                          assesment, trim_type, sleep_diary_directory)

LOdates, GUdates, SleepAnalysisInfo, participant_list = sleep_study.get_in_bed_times()
LOprogramDic = {}
for i in range(0, len(LOdates)):
    LOprogramDic[participant_list[i]] = LOdates[i]
    
#protocol = ps.ProtocolSleepAnalysis(sa_directory, participant_list, study_name, assesment)

#LOprotocol, GUprotocol = protocol.get_study_analysis_sleep_times()
#LOprotocolDic = {}
#for i in range(0, len(LOdates)):
#    LOprotocolDic[participant_list[i]] = LOprotocol[i]
    

error_per_participant = err.get_error_per_participant(LOdates, LOprotocol, participant_list)
error_study, useful_participants = err.get_error_study(
        LOdates, LOprotocol, participant_list)
err.plot_study_error(error_study, useful_participants)

std_per_participant = err.get_std_per_participant(LOdates, LOprotocol, participant_list)


